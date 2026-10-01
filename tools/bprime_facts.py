# -*- coding: utf-8 -*-
"""bprime_facts.py v0（2026-09-30・B′ の転記行 A〜F を、台帳と正本と凍結物から機械で作る・層三の `tools/bl3_facts.py` の型・コーディネータ南無弥勒如来）。

正本 `transcription_rows` のとおり。この版は**凍結の前に決まる行**（A・B・E と F の固定の部分）を作る（`pre`）。行動の下見の値の行 C と、方向と帰無の行 D は、
走行の記録から作る（次の版で足す・値は起動器の記録から読む）。F の走行の時の部分（GPU・ドライバと CUDA の実行時の版・注意の実装と決定性の設定の印字・重みの断片の SHA の照らし）は起動器が記録する。
  - A: 書き出しと揺れの版の割り方・読み取りの集合・台帳の確かめ（自然な続きの割り方を含む）・V3 の確かめの結果と落とした版（`bprime_cells` の台帳から・R07・R08）。
       揺れの版の割り方の境は、版の文字列に選択の文字と refuse を足して割ったとき、版の割り方が保たれ、次のトークンが主の書き出しの次のトークン（台帳の `heads`）と同じ番号であること。
  - B: 升目ごとのプロンプトの長さ・主位置とその字・読み取りの位置・書き出しの並びがプロンプトの中にある位置・その次のトークン（字と番号）・書き出しの最後のトークンの回数・
       その次が refuse の頭の回数。二つの機種の O・Osec・O-Ncold・Osec-Ncold の、腕の本文だけのトークン数とプロンプトの長さと主位置の添字（抽出の二場面・Qwen の側も器で数える・
       Qwen の組み立ては層三の記録の長さと照らす・R07・R25・S28）。
  - E: 順伝播の数（主の計算・両方の向きのために足す分・独立の再計算・道の違いの記述・下見・行動の下見）。組の数は正本から読み、正本の `cost` の数と照らす。
       時間の二つの見込み（バッチ 16 とバッチ一）は、凍結の前の確かめで速さを測ってから足す。
  - F（固定の部分）: 版のピン・softcap の値と読んだ階層・選ぶ層の種類と窓と層の道・「列の長さ ＜ 窓」の assert・取った設定の SHA（手元の目録と照らす）。
**効き目は一つも計算しない**（模型を読まない・順伝播をしない）。
出力: `../records/Bprime/facts-Bprime-pre.json`・`.md`（機械生成・時刻を持たない・再実行で同一バイト）。
用法: python bprime_facts.py pre
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, io, json, glob, math, hashlib, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bprime_gemma as G          # 先に読む（凍結の器の置き場を sys.path に足す）
import bprime_core as P
import bprime_cells as BC

VERSION = 'v0'
BP = os.path.dirname(HERE)
PUB = G.REPO
NL = chr(10)
ToolError = P.ToolError
TWO_MODEL_ARMS = ['O', 'Osec', 'O-Ncold', 'Osec-Ncold']
s16b = lambda b: hashlib.sha256(b).hexdigest().upper()[:16]
s16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
esc = lambda t: t.replace(NL, '⏎')


def load():
    C = json.load(open(os.path.join(BP, 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
    L = json.load(open(os.path.join(HERE, 'ledger-bprime.json'), encoding='utf-8'))
    T3 = json.load(open(os.path.join(PUB, 'design', 'contrasts-Bl3.json'), encoding='utf-8'))
    F3 = json.load(open(os.path.join(PUB, 'records', 'Bl3', 'design-facts-Bl3.json'), encoding='utf-8'))
    return C, L, T3, F3


def subseq(seq, sub):
    return [i for i in range(len(seq) - len(sub) + 1) if list(seq[i:i + len(sub)]) == list(sub)]


# ---------------- 転記行 A ----------------
def row_A(tok, C, L, ids):
    enc = lambda s: tok.encode(s, add_special_tokens=False)
    dec = lambda i: tok.decode([int(i)])
    ids0 = list(L['prefix_ids'])
    rp = C['readout']['primary']
    if enc(L['prefix_text']) != ids0 or L['prefix_text'] != rp['prefix_text'] or ids0 != list(rp['prefix_ids']):
        raise ToolError('書き出しの文字列か割り方が、台帳・正本・トークナイザの間で違う')
    heads = L['heads']
    letters = sorted({x for v in rp['letters'].values() for x in v})
    strings = P.variant_strings(L['prefix_text'])
    var = collections.OrderedDict()
    for name in ('V1', 'V2', 'V3'):
        v = strings[name]
        iv = enc(v)
        bd = collections.OrderedDict()
        for x in letters + ['refuse']:
            e = enc(v + x)
            bd[x] = bool(e[:len(iv)] == iv and len(e) > len(iv) and e[len(iv)] == heads[x]['next'])
        var[name] = {'string': v, 'ids': iv, 'pieces': [dec(i) for i in iv], 'boundary': bd, 'keep': all(bd.values()), 'dropped_why': [] if all(bd.values()) else ['割り方の境が崩れる（選択の文字が一つのトークンに割れない）']}
    iv3 = var['V3']['ids']
    v3_head = max(k for k in range(min(len(ids0), len(iv3)) + 1) if ids0[:k] == iv3[:k])
    v3_seq = {key: len(subseq(d['prompt'], iv3)) for key, d in ids['main'].items()}
    v3_last = {key: sum(1 for t in d['prompt'] if t == iv3[-1]) for key, d in ids['main'].items()}
    v3_checks = {'head_same_tokens': v3_head, 'head_rule': v3_head == len(iv3) - 1, 'seq_in_prompt': sum(v3_seq.values()), 'last_token_in_prompt': sum(v3_last.values())}
    if not v3_checks['head_rule']:
        var['V3']['keep'] = False
        var['V3']['dropped_why'].append('頭の並びが主の書き出しと同じで最後の片だけが違う形でない')
    if v3_checks['seq_in_prompt'] or v3_checks['last_token_in_prompt']:
        var['V3']['keep'] = False
        var['V3']['dropped_why'].append('版の並びか版の最後のトークンがプロンプトの中に現れる')
    fam_sets = {fam: {'letters': ls, 'ids': [heads[x]['next'] for x in ls] + [heads['refuse']['next']], 'pieces': [dec(heads[x]['next']) for x in ls] + [dec(heads['refuse']['next'])]}
                for fam, ls in rp['letters'].items()}
    for key, c in L['cells_main'].items():
        if c['set_ids'] != fam_sets[c['family']]['ids']:
            raise ToolError('台帳の升目の読み取りの集合が族の集合と違う: %s' % key)
    joint = {key: c['joint_tokenization_same'] for key, c in L['cells_main'].items()}
    if not all(joint.values()) or not all(h['stable_prefix'] for h in heads.values()):
        raise ToolError('台帳の割り方の確かめが落ちている')
    kept = [n for n, v in var.items() if v['keep']]
    text = ('主の書き出し %s は %d トークン（%s）。読み取りの集合: %s。書き出しの自然な続きの割り方（台帳）: %s。プロンプトの文字列に書き出しを足して割っても、升目のプロンプトの並びに書き出しの並びを足したものと同じ（%d 升目すべて）。'
            '揺れの版（下見の (iv) だけに使う）: %s。V3 の頭の %d トークンは主の書き出しと同じで、最後の片だけが違う（%s）。V3 の並びがプロンプトに現れる回数 %d・V3 の最後のトークンがプロンプトに現れる回数 %d（主の升目のすべてで数えた）。使う版: %s。'
            ) % (repr(L['prefix_text']), len(ids0), '・'.join('%d「%s」' % (i, esc(dec(i))) for i in ids0),
                 '／'.join('%s: %s' % (fam, '・'.join('%s %d「%s」' % (x, i, esc(p)) for x, i, p in zip(s['letters'] + ['refuse'], s['ids'], s['pieces']))) for fam, s in fam_sets.items()),
                 '・'.join('%s は %d トークン（%s）' % (x, h['n_after'], '・'.join('「%s」' % esc(p) for p in h['pieces_after'])) for x, h in heads.items()),
                 sum(joint.values()),
                 '／'.join('%s %s（%d トークン: %s・割り方の境を%s%s）' % (n, repr(v['string']), len(v['ids']), '・'.join('「%s」' % esc(p) for p in v['pieces']), '保つ' if all(v['boundary'].values()) else '崩す',
                                                                    '' if v['keep'] else '・落とす: ' + '・'.join(v['dropped_why'])) for n, v in var.items()),
                 v3_head, '決まりに合う' if v3_checks['head_rule'] else '**決まりに合わない**', v3_checks['seq_in_prompt'], v3_checks['last_token_in_prompt'], '・'.join(kept) or '無し')
    return {'text': text, 'prefix_ids': ids0, 'sets': fam_sets, 'variants': var, 'v3_checks': v3_checks, 'variants_kept': kept, 'heads': heads}


# ---------------- 転記行 B ----------------
def qwen_tokenizer(T3):
    from transformers import AutoTokenizer
    rev = T3['inputs']['model']['rev']
    snap = os.path.join(os.path.expanduser('~'), '.cache', 'huggingface', 'hub', 'models--' + T3['inputs']['model']['repo'].replace('/', '--'), 'snapshots', rev)
    if not os.path.isdir(snap):
        raise ToolError('Qwen のトークナイザの置き場が無い（層三の登録の版）')
    return AutoTokenizer.from_pretrained(snap), rev


def row_B(tok, tq, C, L, ids, F3):
    import run_stageB_local as RB
    dec = lambda i: tok.decode([int(i)])
    ids0 = list(L['prefix_ids'])
    ref_id = L['heads']['refuse']['next']
    cells = collections.OrderedDict()
    for key, c in L['cells_main'].items():
        pr = ids['main'][key]['prompt']
        if len(pr) != c['prompt_len'] or G.main_position(pr) != c['main_position'] or c['readout_position'] != len(pr) + len(ids0) - 1:
            raise ToolError('升目の並びが台帳と違う: %s' % key)
        occ = subseq(pr, ids0)
        last = [i for i in range(len(pr) - 1) if pr[i] == ids0[-1]]
        cells[key] = {'family': c['family'], 'prompt_len': len(pr), 'main_position': c['main_position'], 'main_token': c['main_position_token'], 'readout_position': c['readout_position'],
                      'prefix_in_prompt_at': occ, 'next_after_prefix': [[pr[i + len(ids0)], dec(pr[i + len(ids0)])] for i in occ if i + len(ids0) < len(pr)],
                      'last_token_in_prompt': len(last), 'refuse_after_last_token': sum(1 for i in last if pr[i + 1] == ref_id)}
    AT = RB.arm_texts()
    two = []
    q_rec = {k: tuple(v) for k, v in ((k, (v['prompt_len'], v['main_position'])) for k, v in F3['facts']['B']['cells'].items())}
    checked = []
    for arm in TWO_MODEL_ARMS:
        for sc in BC.EXTRACT_SCENES:
            scen, inst = RB.scenario_and_instruction(sc)
            um = RB.user_message(AT[arm]['text'], scen['text'], inst)
            g = ids['extract']['%s|%s' % (sc, arm)]
            q = G.apply_chat(tq, um)
            row = {'context': '%s|%s' % (sc, arm), 'gemma_arm_tokens': len(tok.encode(AT[arm]['text'], add_special_tokens=False)) if AT[arm]['text'] else 0,
                   'gemma_prompt_len': len(g), 'gemma_main_position': G.main_position(g),
                   'qwen_arm_tokens': len(tq.encode(AT[arm]['text'], add_special_tokens=False)) if AT[arm]['text'] else 0,
                   'qwen_prompt_len': len(q), 'qwen_main_position': G.main_position(q)}
            if row['context'] in q_rec:
                if (row['qwen_prompt_len'], row['qwen_main_position']) != q_rec[row['context']]:
                    raise ToolError('Qwen の組み立てが層三の記録の長さと違う: %s（%s・記録 %s）' % (row['context'], (row['qwen_prompt_len'], row['qwen_main_position']), q_rec[row['context']]))
                checked.append(row['context'])
            two.append(row)
    if not checked:
        raise ToolError('Qwen の組み立てを層三の記録と一つも照らせなかった')
    text = ('升目ごと（場面 × 土台の腕・括弧は族）: %s。二つの機種の、抽出の二場面の文脈（腕 × 場面）の、腕の本文だけのトークン数・プロンプトの長さ・主位置の添字（Gemma／Qwen）: %s。'
            'Qwen の組み立ては、層三の記録の長さと主位置に一致した（照らした文脈 %s）。') % (
        '／'.join('%s（%s）: 長さ %d・主位置 %d「%s」・読み取り %d・書き出しの並びがプロンプトの中にある位置 %s（次は %s）・書き出しの最後のトークン %d 回（その次が refuse の頭 %d 回）' % (
            k, v['family'], v['prompt_len'], v['main_position'], esc(v['main_token']), v['readout_position'], '・'.join(str(i) for i in v['prefix_in_prompt_at']) or '無し',
            '・'.join('%d「%s」' % (i, esc(p)) for i, p in v['next_after_prefix']) or '無し', v['last_token_in_prompt'], v['refuse_after_last_token']) for k, v in cells.items()),
        '／'.join('%s: Gemma 本文 %d・長さ %d・主位置 %d／Qwen 本文 %d・長さ %d・主位置 %d' % (r['context'], r['gemma_arm_tokens'], r['gemma_prompt_len'], r['gemma_main_position'],
                                                                                r['qwen_arm_tokens'], r['qwen_prompt_len'], r['qwen_main_position']) for r in two),
        '・'.join(checked))
    return {'text': text, 'cells': cells, 'two_models': two, 'qwen_checked_against_bl3': checked}


# ---------------- 転記行 E ----------------
def row_E(C, L):
    named = len(C['directions']['named'])
    iso = int(C['nulls']['isotropic']['count'])
    real = int(C['nulls']['real']['pairs'])
    batch = int(C['readout']['primary']['batch'])
    main_cs = [tuple(x) for x in C['cell_signs_main']]
    rev_cs = [(sc, b, -g) for sc, b, g in main_cs if (sc, b, -g) not in main_cs]
    if len(rev_cs) != C['nulls']['real']['onull_combos']:
        raise ToolError('逆の向きの組の数が正本と違う')
    per_main = named + iso + real + 1
    per_rev = real + 1
    nb = lambda n: math.ceil(n / batch)
    batches16 = len(main_cs) * nb(per_main) + len(rev_cs) * nb(per_rev)
    rows1 = len(main_cs) * per_main + len(rev_cs) * per_rev
    K = C['cost']
    if (per_main, per_rev, nb(per_main), nb(per_rev), batches16) != (K['per_combo'], K['per_reverse'], K['batches_per_combo'], K['batches_per_reverse'], K['batches_16']):
        raise ToolError('本の計算の組の数が正本の `cost` と違う')
    static_rows = [r for r in C['main_rows'] if r['direction'] == 'static']
    nk_rows = [r for r in C['main_rows'] if r['direction'] == 'Nk']
    comps = C['nulls']['real']['comparators_oriented']
    per_row = lambda d: 1 + 1 + iso + int(comps[d])
    n_paths = len(C['independent_recompute']['new_paths'])
    rc_static = n_paths * len(static_rows) * per_row('static')
    rc_nk = n_paths * len(nk_rows) * per_row('Nk')
    M = C['computation']['self_checks']['logit']['measure']
    n_cells = len(C['cells_main'])
    pilot = {'measure_k': M['positions'] * len(M['batches']), 'logit_check': n_cells, 'vi_a': n_cells * 2, 'vi_b': n_cells * (C['pilot']['repeat_n'] - 1),
             'i_ii': n_cells, 'iv': n_cells * 3}                                   # (vi)(b) の一回目は (a) の大きさ一の順伝播を使う（`bprime_run.run_pilot`）
    head = {'logit_check': n_cells, 'layer_check': 1}
    beh = C['behavior_pilot']
    text = ('本の計算: 升目と符号の主の組 %d × 方向 %d（名前のある方向 %d・等方 %d・実在の差 %d）＋ 零のベクトル 一 ＝ 組ごとに %d。逆の向きの組 %d × 実在の差 %d ＋ 零のベクトル 一 ＝ 組ごとに %d。'
            'バッチ %d では、主の組ごとに %d バッチ・逆の向きの組ごとに %d バッチ・あわせて %d バッチ（正本の `cost` の数と器が照らした）。バッチ一では順伝播 %d 回。'
            '独立の再計算（一段目・新しい道 %d × v̂ の行 %d × 〔無操作 ＋ v̂ ＋ 等方 %d ＋ 比べる相手 %d〕）%d 回。Nk の行を入れるなら（案 16・凍結の前に登録者が決める）Nk の行 %d × 道 %d × 〔無操作 ＋ Nk ＋ 等方 %d ＋ 比べる相手 %d〕＝ %d 回を足す。'
            '独立の再抽出 %d 回。道の違いの記述（本の計算がバッチ一に移ったときだけ）はバッチ 16 の道で %d バッチ。'
            '下見の順伝播: 許容の k の測り %d 回（意味のない列の位置 %d × バッチの大きさ %d 通り）・出口の値の自己検査 %d・(vi) の (a) %d（升目ごとにバッチ 16 と一）・(b) %d（升目ごとの繰り返しの二回目から・一回目は (a) の大きさ一）・(i)(ii) %d・(iv) %d（揺れの版三つ × 升目）。本の計算の頭: 出口の値の自己検査 %d・最後の層の自己検査 %d。'
            '行動の下見: 生成 %d 本（升目 %d × %d）。時間の二つの見込み（バッチ 16 とバッチ一）は、凍結の前の確かめで速さを測ってから足す。') % (
        len(main_cs), named + iso + real, named, iso, real, per_main, len(rev_cs), real, per_rev, batch, nb(per_main), nb(per_rev), batches16, rows1,
        n_paths, len(static_rows), iso, int(comps['static']), rc_static, len(nk_rows), n_paths, iso, int(comps['Nk']), rc_nk,
        C['independent_recompute']['reextract']['forwards'], batches16,
        pilot['measure_k'], M['positions'], len(M['batches']), pilot['logit_check'], pilot['vi_a'], pilot['vi_b'], pilot['i_ii'], pilot['iv'], head['logit_check'], head['layer_check'],
        beh['trials_total'], n_cells, beh['trials_per_cell'])
    return {'text': text, 'per_main': per_main, 'per_reverse': per_rev, 'batches_16': batches16, 'forwards_batch1': rows1, 'recompute_static': rc_static, 'recompute_nk_if_added': rc_nk,
            'reextract': C['independent_recompute']['reextract']['forwards'], 'path_difference_batches16': batches16, 'pilot': pilot, 'main_head': head, 'behavior_generations': beh['trials_total']}


# ---------------- 転記行 F（固定の部分） ----------------
def row_F_static(C, L):
    rev = C['inputs']['model']['revision']
    hf = os.path.join(BP, 'hf', 'gemma-4-31B-it', rev)
    man = json.load(open(os.path.join(hf, 'MANIFEST-local.json'), encoding='utf-8'))
    got = {}
    for fn, rec in man['files'].items():
        b = open(os.path.join(hf, fn), 'rb').read()
        h = hashlib.sha256(b).hexdigest()
        if h != rec['sha256'] or len(b) != rec['bytes']:
            raise ToolError('取った設定の SHA が手元の目録と違う: %s' % fn)
        got[fn] = h.upper()[:16]
    cfg = json.load(open(os.path.join(hf, 'config.json'), encoding='utf-8'))
    tc = cfg['text_config']
    lay = C['layers']
    k = int(lay['index'])
    if tc['layer_types'][k] != lay['layer_type'] or cfg.get('final_logit_softcapping') is not None or tc['final_logit_softcapping'] != C['inputs']['model_facts']['final_logit_softcapping']:
        raise ToolError('選ぶ層の種類か softcap の階層が正本と違う')
    max_len = max(c['readout_position'] for c in L['cells_main'].values()) + 1
    if not max_len < tc['sliding_window']:
        raise ToolError('読み取りの列が窓の外')
    shards = sorted(set(json.load(open(os.path.join(hf, 'model.safetensors.index.json'), encoding='utf-8'))['weight_map'].values()))
    shard_sha = [fn for fn in shards if fn in man['files']]
    V = C['inputs']['versions']
    text = ('版の固定: 重みの版 `%s`・transformers %s・torch %s・CUDA %s（ほかに %s を凍結の時に起動器が入れ直して文字列の完全な一致で確かめる）。softcap %s（`text_config` の階層・上の階層には無い）。'
            '選ぶ層の添字 %d（割合 %s の式）の種類は `%s`・窓 %d・層の道 `%s`（読み込んだ模型の `model` の下）。読み取りの列の長さの最大 %d ＜ 窓 %d（assert）。'
            '取った設定の SHA16（手元の目録と一致）: %s。重みの断片 %d 本の SHA-256 は手元の目録に%s（凍結の前に目録を作り、起動器が照らす）。'
            'GPU・ドライバと CUDA の実行時の版・注意の実装と決定性の設定の印字は起動器が記録する（走行の時の部分）。') % (
        rev[:12], V['transformers'], V['torch'], V['cuda'], '・'.join(V['pins_more']), tc['final_logit_softcapping'], k, lay['ratio'], tc['layer_types'][k], tc['sliding_window'], lay['layer_path'], max_len,
        tc['sliding_window'], '・'.join('%s %s' % kv for kv in got.items()), len(shards), ('%d 本ある' % len(shard_sha)) if shard_sha else 'まだ無い')
    return {'text': text, 'config_sha16': got, 'softcap': tc['final_logit_softcapping'], 'layer_index': k, 'layer_type': tc['layer_types'][k], 'window': tc['sliding_window'],
            'max_seq_len': max_len, 'shards': shards, 'shards_in_manifest': len(shard_sha), 'versions': V}


def pre():
    from transformers import AutoTokenizer
    import transformers
    C, L, T3, F3 = load()
    if transformers.__version__ != C['inputs']['versions']['transformers']:
        raise ToolError('transformers の版が固定の版でない（PYTHONPATH に pylib を置く）: %s' % transformers.__version__)
    hf = os.path.join(BP, 'hf', 'gemma-4-31B-it', C['inputs']['model']['revision'])
    tok = AutoTokenizer.from_pretrained(hf)
    tq, qrev = qwen_tokenizer(T3)
    ids = BC.ids_for(tok)
    F = collections.OrderedDict()
    F['A'] = row_A(tok, C, L, ids)
    F['B'] = row_B(tok, tq, C, L, ids, F3)
    F['E'] = row_E(C, L)
    F['F'] = row_F_static(C, L)
    out = {'kind': 'bprime_facts_pre', 'version': VERSION, 'contract_sha16': s16f(os.path.join(BP, 'design', 'contrasts-Bprime.json')), 'ledger_sha16': s16f(os.path.join(HERE, 'ledger-bprime.json')),
           'qwen_revision': qrev, 'transformers': transformers.__version__, 'facts': F,
           'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
    os.makedirs(os.path.join(BP, 'records', 'Bprime'), exist_ok=True)
    jp = os.path.join(BP, 'records', 'Bprime', 'facts-Bprime-pre.json')
    json.dump(out, open(jp, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
    M = ['# B′ の転記行（凍結の前に決まる行・機械生成・`bprime_facts.py` %s・正本 SHA16 %s・台帳 SHA16 %s）' % (VERSION, out['contract_sha16'], out['ledger_sha16']), '',
         '- 効き目は一つも計算していない（模型を読まない・順伝播をしない）。行 C（行動の下見の値）と行 D（方向と帰無）は走行の記録から作る。', ''] + \
        ['- **転記行 %s** — %s' % (k, v['text']) for k, v in F.items()] + ['', out['clause'], '']
    open(os.path.join(BP, 'records', 'Bprime', 'facts-Bprime-pre.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(M))
    print('wrote records/Bprime/facts-Bprime-pre.{json,md} | rows %s | variants kept %s | qwen checked %s | batches16 %d' % (''.join(F), F['A']['variants_kept'], F['B']['qwen_checked_against_bl3'], F['E']['batches_16']))


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if len(sys.argv) >= 2 and sys.argv[1] == 'pre':
        pre()
    else:
        print(__doc__)
