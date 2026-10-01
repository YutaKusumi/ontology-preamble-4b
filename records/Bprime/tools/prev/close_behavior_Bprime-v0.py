# -*- coding: utf-8 -*-
"""close_behavior_Bprime.py v0 —— B′ の行動の下見を閉じる器（正本 `behavior_pilot.order`・`closed_record_keys`・`external_scoring`・草案10 §4.4・R18・S03・T17・T27・
2026-09-30・コーディネータ南無弥勒如来）。

段:
  bundle <出力の置き場> <束の置き場>
      行動の下見の出力（`behavior-trials.json`・`behavior-scored.json`）の SHA-256 を出力の SHA の記録（`end-behavior.json`）と照らし、採点の出力の数（`closing_digests`）と
      升目の集計（`cell_summary`）を出力から計算し直して一字違わず同じことを確かめてから、系統外の模型に見せる束（`bprime_external.bundle`・升目と腕と試行の番号は伏せる）と、
      依頼の文（`request.md`・正本 `behavior_pilot.external_scoring.request_text` に束を並べたもの）と、手元の対応表（`private.json`・送らない）を書く。**送らない**
      （送るのは `send_external_Bprime.py`・送る前に登録者の確認を得る）。
  close <出力の置き場> <束の置き場> <返事の置き場> [--fail "<理由>"]
      同じ確かめをもう一度してから、返事（`response.md`・逐語）を `bprime_external.parse_reply` で読み、器の採点と照らして一致を出し、閉じた記録
      （`records/Bprime/behavior/behavior-closed-Bprime.json`・`.md`）を書く。採点ができなかったとき（呼び出しの失敗・採点の拒否・返事が決まりの形でない）は、
      --fail で理由を与えて閉じる（転記行 C に `fixed_sentences.external_scoring_fail` の文・理由は括弧の中）。返事が決まりの形でないのに --fail が無ければ止める。
  close-tool-error <出力の置き場>
      行動の下見が器の誤りで終わったとき（`behavior-tool-error.json`）。そこまでの記録と印を閉じた記録にする（(iii) は `pilot.iii_fail_sentences.tool_error`・T17）。
閉じた記録の鍵（正本 `behavior_pilot.closed_record_keys`）: 採点の器の SHA（`digests.scorer_sha16`）・採点の出力の SHA（`digests.scores_sha256`）・
生成したトークンの番号の列の SHA（`digests.gen_ids_sha256`）・転記行 C（`row_C`）・起動の記録（`start_record`）・時刻（`closed_jst`）。ほかに、読み取りの下見の起動器が読む
`summaries`・`fixed`・`tool_error` と、集計と報告の器が読む `external`・`iii_status` を置く。記録は一度だけ書く（既にあれば止める）。値の読みは付けない。
DRY の出力（`session.json` の dry が真）は、--allow-dry が無ければ閉じない（合成データの確かめだけに使う）。
用法: python tools/close_behavior_Bprime.py bundle <出力> <束> ／ close <出力> <束> <返事> [--fail 理由] [--out 置き場] ／ close-tool-error <出力> [--out 置き場] ／ --selftest
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, io, json, hashlib, datetime, argparse, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bprime_core as P
import bprime_behavior as BB
import bprime_external as BX

VERSION = 'v0'
NL = chr(10)
JST = datetime.timezone(datetime.timedelta(hours=9))
ToolError = P.ToolError
OUT_DEFAULT = os.path.join(ROOT, 'records', 'Bprime', 'behavior')
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
CANON = os.path.join(ROOT, 'design', 'contrasts-Bprime.json')
KEYMAP = {'採点の器の SHA': 'digests.scorer_sha16', '採点の出力の SHA': 'digests.scores_sha256', '生成したトークンの番号の列の SHA': 'digests.gen_ids_sha256',
          '転記行 C': 'row_C', '起動の記録': 'start_record', '時刻': 'closed_jst'}


def sha256f(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for blk in iter(lambda: fh.read(1 << 22), b''):
            h.update(blk)
    return h.hexdigest().upper()


def sha16f(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]


def load(p):
    with open(p, encoding='utf-8') as fh:
        return json.load(fh)


def _wt(path, text):
    """書いて閉じる（自己検査の合成のファイル・閉じてから SHA を取る）。"""
    with open(path, 'w', encoding='utf-8', newline=NL) as fh:
        fh.write(text)


def write_once(path, text):
    if os.path.exists(path):
        raise ToolError('既にある（一度だけ書く）: %s' % os.path.basename(path))
    with open(path, 'w', encoding='utf-8', newline=NL) as fh:
        fh.write(text)


def canon_json(o):
    return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def read_outputs(C, od, allow_dry=False):
    """行動の下見の出力を読み、SHA と計算し直しで確かめる（落ちたら ToolError）。"""
    end_p = os.path.join(od, 'end-behavior.json')
    if not os.path.exists(end_p):
        raise ToolError('出力の SHA の記録（end-behavior.json）が無い')
    END = load(end_p)
    if END.get('kind') != 'bprime_end_record' or END.get('phase') != 'behavior':
        raise ToolError('出力の SHA の記録が行動の下見のものでない')
    need = ['behavior-scored.json', 'behavior-trials.json']
    got = {fn: sha256f(os.path.join(od, fn)) for fn in need if os.path.exists(os.path.join(od, fn))}
    if sorted(got) != need or any(END['outputs_sha256'].get(fn) != v for fn, v in got.items()):
        raise ToolError('行動の下見の出力が無いか、SHA-256 が出力の SHA の記録と違う')
    S = load(os.path.join(od, 'session.json'))
    if S.get('kind') != 'bprime_colab_behavior':
        raise ToolError('session.json が行動の下見の相のものでない')
    if S.get('dry') and not allow_dry:
        raise ToolError('DRY の出力は閉じない（--allow-dry は合成データの確かめだけ）')
    if not S.get('dry') and S.get('canon_sha16') != sha16f(CANON):
        raise ToolError('行動の下見の正本の SHA16 が今の正本と違う')
    TR = load(os.path.join(od, 'behavior-trials.json'))
    SC = load(os.path.join(od, 'behavior-scored.json'))
    cells = ['%s|%s' % tuple(c) for c in C['cells_main']]
    if list(TR['trials']) != cells or list(SC['scored']) != cells or list(SC['summaries']) != cells or list(SC['roots']) != cells:
        raise ToolError('升目が正本の主の八升目と違う（並びを含む）')
    env = BB.scorer_env()
    dg = BB.closing_digests(TR['trials'], SC['scored'], env)
    if canon_json(dg) != canon_json(SC['digests']):
        raise ToolError('採点の出力の数（採点の器の SHA16・採点の出力の SHA-256・番号の列の SHA-256）を計算し直した値が出力と違う')
    for key in cells:
        s_ = BB.cell_summary(C, key, TR['trials'][key], SC['scored'][key], SC['roots'][key])
        if canon_json(s_) != canon_json(SC['summaries'][key]):
            raise ToolError('升目の集計を計算し直した値が出力と違う: %s' % key)
    start = sorted(fn for fn in os.listdir(od) if fn.startswith('start-behavior') and fn.endswith('.json'))
    if len(start) != 1:
        raise ToolError('起動の記録（start-behavior.json）がちょうど一つでない')
    return {'END': END, 'S': S, 'TR': TR, 'SC': SC, 'env': env, 'digests': dg, 'cells': cells, 'start': start[0], 'outputs_sha256': got}


def families(C, cells):
    return {k: BB.sent_of(k)[1] for k in cells}


def do_bundle(C, od, bd, allow_dry=False):
    R = read_outputs(C, od, allow_dry)
    os.makedirs(bd, exist_ok=True)
    items, private = BX.bundle(C, R['TR']['trials'], families(C, R['cells']))
    req = BX.request_text(C, items)
    write_once(os.path.join(bd, 'items.json'), json.dumps({'items': items, 'clause': CLAUSE}, ensure_ascii=False, indent=1) + NL)
    write_once(os.path.join(bd, 'private.json'), json.dumps({'private': private, 'outputs_sha256': R['outputs_sha256'], 'clause': CLAUSE}, ensure_ascii=False, indent=1) + NL)
    write_once(os.path.join(bd, 'request.md'), req)
    return {'n': len(items), 'request_sha16': sha16f(os.path.join(bd, 'request.md')), 'items_sha16': sha16f(os.path.join(bd, 'items.json'))}


def seeds_of(C, TR):
    out = collections.OrderedDict()
    for key, ts in TR['trials'].items():
        batches = collections.OrderedDict()
        for t in ts:
            b = batches.setdefault(t['batch_index'], {'batch_index': t['batch_index'], 'batch_seed': t['batch_seed'], 'rows': t['batch_rows'], 'trials': []})
            b['trials'].append(t['trial_index'])
        out[key] = {'cell_seed': ts[0]['cell_seed'] if ts else None, 'batches': list(batches.values())}
    return {'rule': C['behavior_pilot']['seeds']['rule'], 'per_row': C['behavior_pilot']['seeds']['per_row'], 'cells': out}


def row_c(C, R, external):
    SC = R['SC']
    cells = collections.OrderedDict()
    for key in R['cells']:
        s = SC['summaries'][key]
        cells[key] = dict(s, root_sentence=P.root_sentence_choice(s['root_counts']))
    U = C['behavior_pilot']['scoring']['unscorable']
    return collections.OrderedDict([
        ('cells', cells),
        ('unscorable_exceeds', P.unscorable_exceeds({k: (v['unscorable'], v['n']) for k, v in SC['summaries'].items()}, U)),
        ('sampling', R['TR'].get('fixed')),
        ('seeds', seeds_of(C, R['TR'])),
        ('decode', {'rule': C['behavior_pilot']['decode']['rule'], 'versions': {k: (R['S'].get('versions') or {}).get(k) for k in ('transformers', 'tokenizers')}}),
        ('gen_ids_sha256', R['digests']['gen_ids_sha256']),
        ('external', external),
    ])


def do_close(C, od, bd, rd, fail=None, out_dir=OUT_DEFAULT, allow_dry=False, now=None):
    R = read_outputs(C, od, allow_dry)
    items = load(os.path.join(bd, 'items.json'))['items']
    PV = load(os.path.join(bd, 'private.json'))
    if PV['outputs_sha256'] != R['outputs_sha256']:
        raise ToolError('束を作った出力と、閉じる出力が違う')
    items2, private2 = BX.bundle(C, R['TR']['trials'], families(C, R['cells']))
    if canon_json(items2) != canon_json(items) or canon_json(private2) != canon_json(PV['private']):
        raise ToolError('束を作り直した値が、束の置き場の束と違う')
    req_sha16 = sha16f(os.path.join(bd, 'request.md'))
    if BX.request_text(C, items) != open(os.path.join(bd, 'request.md'), encoding='utf-8').read():
        raise ToolError('依頼の文を作り直した値が、束の置き場の依頼の文と違う')
    ext = collections.OrderedDict([('name', C['behavior_pilot']['external_scoring']['print_name']), ('request_sha16', req_sha16), ('n_items', len(items))])
    if fail is None:
        rp = os.path.join(rd, 'response.md')
        meta_p = os.path.join(rd, 'meta.json')
        if not (os.path.exists(rp) and os.path.exists(meta_p)):
            raise ToolError('返事（response.md）か呼び出しの記録（meta.json）が無い（採点ができなかったときは --fail で理由を与える）')
        M = load(meta_p)
        if M.get('request_sha16') != req_sha16:
            raise ToolError('呼び出しの記録の依頼の文の SHA16 が、束の依頼の文と違う')
        try:
            parsed = BX.parse_reply(open(rp, encoding='utf-8').read(), [it['id'] for it in items])
        except (ToolError, ValueError) as e_:
            raise ToolError('返事が決まりの形でない（採点ができなかったときは --fail で理由を与える）: %s' % e_)
        ag = BX.agreement(parsed, PV['private'], R['SC']['scored'])
        ext.update(lineage=M.get('model_returned'), model_requested=M.get('model_requested'), system_fingerprint=M.get('system_fingerprint'), reply_sha16=sha16f(rp),
                   n=ag['n'], agree=ag['agree'], share=ag['share'], by_field=ag['by_field'], rows=ag['rows'])
    else:
        ext.update(fail=C['fixed_sentences']['external_scoring_fail'].replace('（理由）', '（%s）' % fail), reason=fail)
    iii = BB.iii_status(C, R['SC']['summaries'])
    t = now or datetime.datetime.now(JST)
    rec = collections.OrderedDict([
        ('kind', 'bprime_behavior_closed'), ('version', VERSION), ('closed_jst', t.isoformat(timespec='seconds')), ('tool_error', False),
        ('contract_sha16', sha16f(CANON)), ('session', {k: R['S'].get(k) for k in ('session_id', 'commit', 'dry', 'gpu', 'versions', 'canon_sha16', 'determinism')}),
        ('start_record', {'file': R['start'], 'sha256': sha256f(os.path.join(od, R['start']))}), ('end_record', {'file': 'end-behavior.json', 'sha256': sha256f(os.path.join(od, 'end-behavior.json'))}),
        ('outputs_sha256', R['outputs_sha256']), ('digests', R['digests']), ('summaries', R['SC']['summaries']), ('fixed', R['TR'].get('fixed')),
        ('iii_status', {k: v for k, v in iii.items() if k != 'rate'}), ('external', ext), ('row_C', row_c(C, R, ext)),
        ('bundle', {'items_sha16': sha16f(os.path.join(bd, 'items.json')), 'private_sha16': sha16f(os.path.join(bd, 'private.json')), 'request_sha16': req_sha16}),
        ('closed_record_keys', KEYMAP), ('clause', CLAUSE)])
    return write_closed(C, rec, out_dir)


def do_close_tool_error(C, od, out_dir=OUT_DEFAULT, allow_dry=False, now=None):
    ep = os.path.join(od, 'behavior-tool-error.json')
    end_p = os.path.join(od, 'end-behavior.json')
    if not (os.path.exists(ep) and os.path.exists(end_p)):
        raise ToolError('器の誤りの記録（behavior-tool-error.json）か出力の SHA の記録が無い')
    END = load(end_p)
    if END.get('outputs_sha256', {}).get('behavior-tool-error.json') != sha256f(ep):
        raise ToolError('器の誤りの記録の SHA-256 が出力の SHA の記録と違う')
    S = load(os.path.join(od, 'session.json'))
    if S.get('dry') and not allow_dry:
        raise ToolError('DRY の出力は閉じない')
    start = sorted(fn for fn in os.listdir(od) if fn.startswith('start-behavior') and fn.endswith('.json'))
    t = now or datetime.datetime.now(JST)
    E = load(ep)
    rec = collections.OrderedDict([
        ('kind', 'bprime_behavior_closed'), ('version', VERSION), ('closed_jst', t.isoformat(timespec='seconds')), ('tool_error', True), ('tool_error_message', E.get('tool_error')),
        ('contract_sha16', sha16f(CANON)), ('session', {k: S.get(k) for k in ('session_id', 'commit', 'dry', 'gpu', 'versions', 'canon_sha16', 'determinism')}),
        ('start_record', {'file': start[0], 'sha256': sha256f(os.path.join(od, start[0]))} if len(start) == 1 else None),
        ('end_record', {'file': 'end-behavior.json', 'sha256': sha256f(end_p)}), ('outputs_sha256', {'behavior-tool-error.json': sha256f(ep)}),
        ('digests', None), ('summaries', None), ('fixed', None), ('iii_status', {'status': 'tool_error', 'sentence': C['pilot']['iii_fail_sentences']['tool_error']}),
        ('external', None), ('row_C', {'tool_error': C['pilot']['iii_fail_sentences']['tool_error']}), ('closed_record_keys', KEYMAP), ('clause', CLAUSE)])
    return write_closed(C, rec, out_dir)


def write_closed(C, rec, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    jp = os.path.join(out_dir, 'behavior-closed-Bprime.json')
    mp = os.path.join(out_dir, 'behavior-closed-Bprime.md')
    if os.path.exists(jp) or os.path.exists(mp):
        raise ToolError('閉じた記録は既にある（一度だけ書く）')
    for k, path in KEYMAP.items():
        x = rec
        for part in path.split('.'):
            x = (x or {}).get(part) if isinstance(x, dict) else None
        if k not in C['behavior_pilot']['closed_record_keys'] or (x is None and not (rec['tool_error'] and path.startswith('digests'))):
            raise ToolError('閉じた記録の鍵が欠けた: %s' % k)
    write_once(jp, json.dumps(rec, ensure_ascii=False, indent=1) + NL)
    write_once(mp, render_md(C, rec, sha16f(jp)))
    return jp, mp


def fmt(x, nd=4):
    if x is None:
        return '—'
    if isinstance(x, float):
        return ('%.' + str(nd) + 'f') % x
    return str(x)


def render_md(C, rec, json_sha16):
    L = ['# B′ の行動の下見の閉じた記録（機械生成・`tools/close_behavior_Bprime.py` %s）' % VERSION, '',
         '- 閉じた時刻: %s（日本時間）・記録 `behavior-closed-Bprime.json`（SHA16 %s）・正本 SHA16 %s。' % (rec['closed_jst'], json_sha16, rec['contract_sha16']),
         '- 起動の記録: `%s`（SHA-256 %s）・出力の SHA の記録: `%s`（SHA-256 %s）。' % ((rec['start_record'] or {}).get('file'), (rec['start_record'] or {}).get('sha256'),
                                                                               rec['end_record']['file'], rec['end_record']['sha256']),
         '- セッション: コミット %s・GPU %s・DRY %s。' % (rec['session'].get('commit'), rec['session'].get('gpu'), rec['session'].get('dry'))]
    if rec['tool_error']:
        L += ['- **器の誤りで終わった**: %s。(iii) は「%s」。' % (rec.get('tool_error_message'), rec['iii_status']['sentence']), '', CLAUSE, '']
        return NL.join(L)
    d = rec['digests']
    L += ['- 採点の器の SHA16: %s。採点の出力の SHA-256: %s。生成したトークンの番号の列の SHA-256: %s（試行 %d）。' % (
        '・'.join('%s %s' % kv for kv in sorted(d['scorer_sha16'].items())), d['scores_sha256'], d['gen_ids_sha256'], d['n_trials']),
          '- (iii) に渡す状態: %s%s。' % (rec['iii_status']['status'], ('（升目 %s）' % '・'.join(rec['iii_status'].get('cells') or [])) if rec['iii_status'].get('cells') else ''), '',
          '## 転記行 C（升目ごと・分母は升目の試行の全件・率は記述）', '',
          '| 升目 | 試行 | 破局 | 主の率 | Wilson 95% | refuse | 書式外 | JSON 直答 | 上限で切れた | 切れたものを除いた率 | 採点できなかった（上限で切れた・採点の器の例外） | 定型の文 |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|']
    for key, c in rec['row_C']['cells'].items():
        rs = c['root_sentence']
        L.append('| %s | %d | %d | %s | %s〜%s | %d | %d | %d | %d | %s | %d（%d・%d） | %s%s |' % (
            key.replace('|', '\\|'), c['n'], c['catastrophe'], fmt(c['rate']), fmt(c['wilson95'][0]), fmt(c['wilson95'][1]), c['refuse'], c['format_fail'], c['json_direct'],
            c['truncated'], fmt(c['rate_excl_truncated']), c['unscorable'], c['unscorable_by_reason'].get('truncated', 0), c['unscorable_by_reason'].get('scorer_error', 0),
            rs['main'], '・four' if rs['four'] else ''))
    L += ['', '## 書き出しの根の件数（升目ごと・転記行 C）', '',
          '| 升目 | (a) 文字列 | (a) 番号 | (d) 頭の七つ | 鍵が二つ以上 | (b) 区分 | (b) 起点の決まり |', '|---|---|---|---|---|---|---|']
    for key, c in rec['row_C']['cells'].items():
        r = c['root_counts']
        L.append('| %s | %s | %s | %s | %s | %s | %s |' % (key.replace('|', '\\|'), r.get('a_str'), ('器の誤りで数えられなかった' if r.get('a_tok_error') else r.get('a_tok')), r.get('d'),
                                                        r.get('multi_key'), '・'.join('%s %s' % kv for kv in (r.get('classes') or {}).items()),
                                                        '・'.join('%s %s' % kv for kv in (r.get('key_rule') or {}).items())))
    ex = rec['external']
    L += ['', '## %s' % ex['name'], '']
    if 'fail' in ex:
        L.append('- %s' % ex['fail'])
    else:
        L.append('- 系譜: 返事の模型 %s（依頼 %s・system_fingerprint %s）。依頼の文の SHA16 %s・返事の SHA16 %s。' % (ex.get('lineage'), ex.get('model_requested'), ex.get('system_fingerprint'),
                                                                                       ex['request_sha16'], ex.get('reply_sha16')))
        L.append('- 一致: %d 件中 %d 件（書式外か %d・選択 %d・破局 %d）。一致の記述で、妥当性の測定ではない。' % (ex['n'], ex['agree'], ex['by_field']['format'], ex['by_field']['choice'], ex['by_field']['catastrophe']))
    sm = rec['row_C']['sampling'] or {}
    L += ['', '## 標本化・種・復号（転記行 C）', '',
          '- 解決された設定（`generate` の中で取った値の要約）: `%s`' % json.dumps(sm, ensure_ascii=False, sort_keys=True).replace('`', "'"),
          '- 種: %s' % rec['row_C']['seeds']['per_row'],
          '- 復号: %s・版 %s。' % (rec['row_C']['decode']['rule'], '・'.join('%s %s' % kv for kv in rec['row_C']['decode']['versions'].items())),
          '', CLAUSE, '']
    return NL.join(L)


# ---------------- 自己検査（合成の出力） ----------------
def _synthetic_outputs(C, od, dry=True, tamper=False):
    """合成の行動の下見の出力（`dry_bprime_behavior` の合成の応答を升目の族に合わせて 40 件ずつ並べる・本物のトークナイザで番号にする）。"""
    import dry_bprime_behavior as DB
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(DB.HF)
    env = BB.scorer_env()
    strings = P.variant_strings(DB.LEDGER['prefix_text'])
    window = C['behavior_pilot']['root_counts']['b']['window_chars']
    surv = ['direct_a', 'amount_zero_a', 'refuse_json', 'reasoning_then_json', 'two_blocks_json_multi', 'unclosed_block', 'truncated_after_json', 'v1_only', 'prose_refusal', 'headings_format']
    nuc = ['nuclear_esc4', 'nuclear_a_low_esc', 'nuclear_refuse', 'prose_refusal']
    trials, scored, roots, summaries = (collections.OrderedDict() for _ in range(4))
    for ci, (sc, arm) in enumerate(C['cells_main']):
        key = '%s|%s' % (sc, arm)
        fam = BB.sent_of(key)[1]
        names = nuc if fam == 'nuclear' else surv
        T_, S_, R_ = [], [], []
        for i in range(int(C['behavior_pilot']['trials_per_cell'])):
            nm = names[(i + ci) % len(names)]
            _, text, finish, _ = DB.CASES[nm]
            if fam == 'nuclear' and nm == 'prose_refusal':
                text = 'この判断には協力できません。'
            ids = tok.encode(text, add_special_tokens=False)
            t = {'cell': key, 'trial_index': i, 'batch_index': i // 8, 'batch_pos': i % 8, 'batch_rows': 8, 'batch_seed': 1000 * ci + i // 8, 'cell_seed': 92004 + ci,
                 'gen_ids': ids, 'finish': finish, 'stop_token': None if finish == 'length' else 106, 'n_tokens': len(ids), 'text': BB.decode(tok, ids)}
            sent, fam_ = BB.sent_of(key)
            T_.append(t)
            S_.append(BB.score_trial(t, fam_, sent, env))
            R_.append(BB.root_counts_trial(t, [2, 105, 2364, 107], [int(x) for x in DB.LEDGER['cells_main'][key]['set_ids']], DB.LEDGER['prefix_ids'], strings, window, env['parser_mod']))
        trials[key], scored[key], roots[key] = T_, S_, R_
        summaries[key] = BB.cell_summary(C, key, T_, S_, R_)
    digests = BB.closing_digests(trials, scored, env)
    os.makedirs(od, exist_ok=True)

    def wj(fn, o):
        with open(os.path.join(od, fn), 'w', encoding='utf-8', newline=NL) as fh:
            fh.write(json.dumps(o, ensure_ascii=False, indent=1) + NL)
    wj('behavior-trials.json', {'trials': trials, 'calls': {}, 'fixed': {'processors': ['合成'], 'do_sample': True}, 'clause': CLAUSE})
    wj('behavior-scored.json', {'scored': scored, 'roots': roots, 'summaries': summaries, 'digests': digests, 'clause': CLAUSE})
    wj('session.json', {'kind': 'bprime_colab_behavior', 'dry': dry, 'commit': 'dry', 'gpu': 'dry', 'versions': {'transformers': '5.16.1', 'tokenizers': 'x'}, 'canon_sha16': sha16f(CANON)})
    wj('start-behavior.json', {'kind': 'bprime_start_record', 'phase': 'behavior'})
    if tamper:
        summaries[list(summaries)[0]]['catastrophe'] += 1
        wj('behavior-scored.json', {'scored': scored, 'roots': roots, 'summaries': summaries, 'digests': digests, 'clause': CLAUSE})
    wj('end-behavior.json', {'kind': 'bprime_end_record', 'phase': 'behavior', 'outputs_sha256': {fn: sha256f(os.path.join(od, fn)) for fn in ('behavior-trials.json', 'behavior-scored.json')}})
    return scored


def _selftest():
    import tempfile
    C = load(CANON)
    ok = []
    with tempfile.TemporaryDirectory() as td:
        od, bd, rd, out = (os.path.join(td, x) for x in ('out', 'bundle', 'reply', 'closed'))
        scored = _synthetic_outputs(C, od)
        try:
            do_bundle(C, od, bd)
            ok.append(('DRY の出力は --allow-dry が無ければ束にしない', False))
        except ToolError:
            ok.append(('DRY の出力は --allow-dry が無ければ束にしない', True))
        b = do_bundle(C, od, bd, allow_dry=True)
        items = load(os.path.join(bd, 'items.json'))['items']
        PV = load(os.path.join(bd, 'private.json'))['private']
        ok.append(('束の数が正本の数', b['n'] == C['behavior_pilot']['external_scoring']['n'] and len(items) == len(PV)))
        req = open(os.path.join(bd, 'request.md'), encoding='utf-8').read()
        ok.append(('依頼の文に升目と腕の名が無い', not any(('%s|%s' % tuple(c)) in req for c in C['cells_main']) and 'O-Ncold' not in req and 'Onull' not in req))
        # 返事を合成する（器の採点のとおり・一件だけ選択を違える）
        os.makedirs(rd)
        lines = []
        for j, it in enumerate(items):
            key, ti = PV[it['id']]
            s = scored[key][ti]['score']
            o = {'id': it['id'], 'format': '書式外' if (s is None or s['format_fail']) else 'ok', 'choice': None if s is None else s['choice'], 'catastrophe': None if s is None else s['catastrophe']}
            if j == 0:
                o['choice'] = 'zz'
            lines.append(json.dumps(o, ensure_ascii=False))
        _wt(os.path.join(rd, 'response.md'), NL.join(lines) + NL)
        _wt(os.path.join(rd, 'meta.json'), json.dumps({'model_requested': 'grok-4.7', 'model_returned': 'grok-4.7-合成', 'system_fingerprint': 'fp_合成',
                                                        'request_sha16': b['request_sha16']}, ensure_ascii=False))
        t0 = datetime.datetime(2026, 9, 30, 12, 0, tzinfo=JST)
        jp, mp = do_close(C, od, bd, rd, out_dir=out, allow_dry=True, now=t0)
        R = load(jp)
        ok.append(('一致は一件だけ違う', R['external']['agree'] == R['external']['n'] - 1 and R['external']['by_field']['choice'] == R['external']['n'] - 1))
        ok.append(('閉じた記録の鍵がそろう', all(k in C['behavior_pilot']['closed_record_keys'] for k in KEYMAP) and R['row_C']['cells'] and R['digests']['gen_ids_sha256']))
        ok.append(('(iii) の状態が決まりの内', R['iii_status']['status'] in ('ok', 'unscorable')))
        ok.append(('上限で切れた応答は分子に数えない', all(c['catastrophe'] <= c['n'] - 0 for c in R['row_C']['cells'].values())))
        try:
            do_close(C, od, bd, rd, out_dir=out, allow_dry=True, now=t0)
            ok.append(('二度目は書かない', False))
        except ToolError:
            ok.append(('二度目は書かない', True))
        # 決まりの形でない返事は --fail が無ければ止め、--fail で閉じる
        rd2, out2 = os.path.join(td, 'reply2'), os.path.join(td, 'closed2')
        os.makedirs(rd2)
        _wt(os.path.join(rd2, 'response.md'), '採点できません。')
        _wt(os.path.join(rd2, 'meta.json'), json.dumps({'request_sha16': b['request_sha16']}))
        try:
            do_close(C, od, bd, rd2, out_dir=out2, allow_dry=True, now=t0)
            ok.append(('決まりの形でない返事で止まる', False))
        except ToolError:
            ok.append(('決まりの形でない返事で止まる', True))
        jp2, _ = do_close(C, od, bd, rd2, fail='採点の拒否', out_dir=out2, allow_dry=True, now=t0)
        ok.append(('--fail で閉じ、失敗の文を置く', load(jp2)['external']['fail'] == '系統外の模型による採点ができなかった（採点の拒否）'))
        # 出力の書き換えで止まる
        od3 = os.path.join(td, 'out3')
        _synthetic_outputs(C, od3, tamper=True)
        try:
            do_bundle(C, od3, os.path.join(td, 'b3'), allow_dry=True)
            ok.append(('升目の集計の書き換えで止まる', False))
        except ToolError:
            ok.append(('升目の集計の書き換えで止まる', True))
        # 器の誤りで閉じる
        od4 = os.path.join(td, 'out4')
        os.makedirs(od4)
        _wt(os.path.join(od4, 'behavior-tool-error.json'), json.dumps({'tool_error': '合成の誤り'}, ensure_ascii=False))
        _wt(os.path.join(od4, 'session.json'), json.dumps({'kind': 'bprime_colab_behavior', 'dry': True}))
        _wt(os.path.join(od4, 'start-behavior.json'), '{}')
        _wt(os.path.join(od4, 'end-behavior.json'), json.dumps({'kind': 'bprime_end_record', 'phase': 'behavior',
                                                                'outputs_sha256': {'behavior-tool-error.json': sha256f(os.path.join(od4, 'behavior-tool-error.json'))}}))
        jp4, mp4 = do_close_tool_error(C, od4, out_dir=os.path.join(td, 'closed4'), allow_dry=True, now=t0)
        R4 = load(jp4)
        ok.append(('器の誤りで閉じた記録', R4['tool_error'] is True and R4['iii_status']['status'] == 'tool_error' and '較正できなかった' in open(mp4, encoding='utf-8').read()))
        md = open(mp, encoding='utf-8').read()
        ok.append(('記録の表の升目の縦棒を逃がす', '| N1\\|O-Ncold |' in md))
    bad = [n for n, v in ok if not v]
    assert not bad, bad
    print('close_behavior_Bprime.py %s SELFTEST PASS（%d 項目）' % (VERSION, len(ok)))


def main():
    sys.stdout.reconfigure(encoding='utf-8')          # 包み直さない（合成データの器が読み込みのときに包み直すので、二重に包むと先の包みが閉じる）
    if '--selftest' in sys.argv:
        return _selftest()
    ap = argparse.ArgumentParser()
    ap.add_argument('stage', choices=['bundle', 'close', 'close-tool-error'])
    ap.add_argument('paths', nargs='+')
    ap.add_argument('--fail')
    ap.add_argument('--out', default=OUT_DEFAULT)
    ap.add_argument('--allow-dry', action='store_true')
    a = ap.parse_args()
    C = load(CANON)
    if a.stage == 'bundle':
        print('[close_behavior_Bprime] 束: %s' % do_bundle(C, a.paths[0], a.paths[1], a.allow_dry))
    elif a.stage == 'close':
        jp, mp = do_close(C, a.paths[0], a.paths[1], a.paths[2] if len(a.paths) > 2 else None, fail=a.fail, out_dir=a.out, allow_dry=a.allow_dry)
        print('[close_behavior_Bprime] 閉じた記録: %s（SHA16 %s）・%s' % (jp, sha16f(jp), mp))
    else:
        jp, mp = do_close_tool_error(C, a.paths[0], out_dir=a.out, allow_dry=a.allow_dry)
        print('[close_behavior_Bprime] 器の誤りで閉じた記録: %s（SHA16 %s）' % (jp, sha16f(jp)))


if __name__ == '__main__':
    main()
