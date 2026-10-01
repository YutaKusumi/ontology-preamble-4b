# -*- coding: utf-8 -*-
"""close_behavior_Bprime.py v0.2 —— B′ の行動の下見を閉じる器（正本 `behavior_pilot.order`・`closed_record_keys`・`external_scoring`・草案10 §4.4・R18・S03・T17・T27・
2026-09-30・コーディネータ南無弥勒如来）。

段:
  bundle <出力の置き場> <束の置き場>
      行動の下見の出力（`behavior-trials.json`・`behavior-scored.json`）の SHA-256 を出力の SHA の記録（`end-behavior-<セッションの頭の 8 字>.json`・ちょうど一つ）と照らし、
      試行ごとの採点を当て直し（v0.2・U26）、採点の出力の数（`closing_digests`）と升目の集計（`cell_summary`）を出力から計算し直して一字違わず同じことを確かめてから、系統外の模型に見せる束（`bprime_external.bundle`・升目と腕と試行の番号は伏せる）と、
      依頼の文（`request.md`・正本 `behavior_pilot.external_scoring.request_text` に束を並べたもの）と、手元の対応表（`private.json`・送らない）を書く。**送らない**
      （送るのは `send_external_Bprime.py`・送る前に登録者の確認を得る）。
  close <出力の置き場> <束の置き場> <返事の置き場> [--fail "<理由>"]
      同じ確かめをもう一度してから、返事（`response.md`・逐語）を `bprime_external.parse_reply` で読み、器の採点と照らして一致を出し、閉じた記録
      （`records/Bprime/behavior/behavior-closed-Bprime.json`・`.md`）を書く。採点ができなかったとき（呼び出しの失敗・採点の拒否・返事が決まりの形でない）は、
      --fail で理由を与えて閉じる（転記行 C に `fixed_sentences.external_scoring_fail` の文・理由は括弧の中）。返事が決まりの形でないのに --fail が無ければ止める。
      理由は閉じた一覧（呼び出しの失敗・採点の拒否・返事が決まりの形でない）から選ぶ（v0.2・U07）。依頼の文と返事は改行を訳さずに読み、SHA はバイトで取る（v0.2・U13）。
  close-tool-error <出力の置き場>
      行動の下見が器の誤りで終わったとき（`behavior-tool-error.json`）。そこまでの記録と印を閉じた記録にする（(iii) は `pilot.iii_fail_sentences.tool_error`・T17）。
      系統外の採点は「行動の下見が器の誤りで終わった」を理由にした失敗の文を、閉じた記録と転記行 C に置く（v0.2・U07）。
やり直し（--rerun・正本 `behavior_pilot.rerun`・v0.2）: 器の誤りで閉じた記録があり、読み取りの下見の走行がまだ無く、凍結の記録の台帳にやり直しの行（kind behavior_rerun）が
  やり直しの数だけあるときだけ。一度目の閉じた記録は `behavior-closed-Bprime-prior-<セッションの頭の 8 字>.json`・`.md` にバイトのまま写して並べ（置き換えない）、
  新しい閉じた記録の `prior_closed` に並べる（報告の頭に並べて使わない・S11・T16）。
閉じた記録の鍵（正本 `behavior_pilot.closed_record_keys`）: 採点の器の SHA（`digests.scorer_sha16`）・採点の出力の SHA（`digests.scores_sha256`）・
生成したトークンの番号の列の SHA（`digests.gen_ids_sha256`）・転記行 C（`row_C`）・起動の記録（`start_record`）・時刻（`closed_jst`）。ほかに、読み取りの下見の起動器が読む
`summaries`・`fixed`・`tool_error` と、集計と報告の器が読む `external`・`iii_status` を置く。記録は一度だけ書く（既にあれば止める）。値の読みは付けない。
DRY の出力（`session.json` の dry が真）は、--allow-dry が無ければ閉じない（合成データの確かめだけに使う）。
用法: python tools/close_behavior_Bprime.py bundle <出力> <束> ／ close <出力> <束> <返事> [--fail 理由] [--out 置き場] [--rerun --freeze 凍結の記録] ／
  close-tool-error <出力> [--out 置き場] [--rerun --freeze 凍結の記録] ／ --selftest
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, io, json, shutil, hashlib, datetime, argparse, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bprime_core as P
import bprime_behavior as BB
import bprime_external as BX

VERSION = 'v0.2'        # v0.2（2026-09-30・器の実装の検分の後）: 起動の記録と出力の SHA の記録の名にセッション（`start-behavior-*`・`end-behavior-*` をちょうど一つ・U09）・依頼の文と返事を改行を訳さずに読み、SHA はバイトで（U13）・試行ごとの採点の当て直し（U26）・器の誤りで閉じた記録に系統外の採点ができなかった文（U07）・--fail の理由を閉じた一覧から（U07）・やり直しの道（U07・U09）。前の版は `prev/close_behavior_Bprime-v0.1.py`／v0.1（2026-09-30）: 出力の置き場の起動の記録の写しの SHA-256 を session.json の値（start_sha256）と照らす（起動器 v0.2 が写しを置く・K19）。前の版は `prev/close_behavior_Bprime-v0.py`
NL = chr(10)
JST = datetime.timezone(datetime.timedelta(hours=9))
ToolError = P.ToolError
OUT_DEFAULT = os.path.join(ROOT, 'records', 'Bprime', 'behavior')
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
CANON = os.path.join(ROOT, 'design', 'contrasts-Bprime.json')
FR_DEFAULT = os.path.join(ROOT, 'records', 'Bprime', 'FREEZE-RECORD-Bprime.json')
FAIL_REASONS = ('呼び出しの失敗', '採点の拒否', '返事が決まりの形でない')          # --fail が受ける理由の閉じた一覧（正本 v5 `behavior_pilot.external_scoring.fail_reasons` と同じことを自己検査で照らす・v0.2・U07・U29）
TOOL_ERROR_REASON = '行動の下見が器の誤りで終わった'                                # 器の誤りで閉じたときの理由（正本 v5 `behavior_pilot.external_scoring.tool_error_reason`・v0.2・U07）


def fail_sentence(C, reason):
    """系統外の模型による採点ができなかった文（正本 v5 `fixed_sentences.external_scoring_fail` の〔理由〕を埋める・v0.2・U29）。"""
    return P.fill(C['fixed_sentences']['external_scoring_fail'], {'理由': reason})
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


def sha16raw(p):
    """ファイルのバイトの SHA-256 の先頭 16 字（改行を直さない・依頼の文と返事に使う・送る器の `read_request` と同じ・v0.2・U13）。"""
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest().upper()[:16]


def read_raw(p):
    """改行を訳さずに読む（\r も \r\n もそのまま・v0.2・U13）。"""
    with open(p, 'rb') as fh:
        return fh.read().decode('utf-8')


def one_file(od, prefix):
    """出力の置き場の `<prefix>*.json` がちょうど一つならその名（v0.2・U09・名はセッションつき）。"""
    got = sorted(fn for fn in os.listdir(od) if fn.startswith(prefix) and fn.endswith('.json'))
    if len(got) != 1:
        raise ToolError('%s*.json がちょうど一つでない（%d）' % (prefix, len(got)))
    return got[0]


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
    end_fn = one_file(od, 'end-behavior')
    END = load(os.path.join(od, end_fn))
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
    if not S.get('session_id') or END.get('session') != S.get('session_id'):
        raise ToolError('出力の SHA の記録のセッションが session.json と違う（v0.2・U09）')
    if not S.get('dry') and S.get('canon_sha16') != sha16f(CANON):
        raise ToolError('行動の下見の正本の SHA16 が今の正本と違う')
    TR = load(os.path.join(od, 'behavior-trials.json'))
    SC = load(os.path.join(od, 'behavior-scored.json'))
    cells = ['%s|%s' % tuple(c) for c in C['cells_main']]
    if list(TR['trials']) != cells or list(SC['scored']) != cells or list(SC['summaries']) != cells or list(SC['roots']) != cells:
        raise ToolError('升目が正本の主の八升目と違う（並びを含む）')
    env = BB.scorer_env()
    for key in cells:                                                     # 試行ごとの採点を当て直す（CPU で安い・v0.2・U26）
        fam_, sent_ = BB.sent_of(key)[1], BB.sent_of(key)[0]
        if len(TR['trials'][key]) != len(SC['scored'][key]):
            raise ToolError('試行と採点の数が違う: %s' % key)
        for i, t in enumerate(TR['trials'][key]):
            if canon_json(BB.score_trial(t, fam_, sent_, env)) != canon_json(SC['scored'][key][i]):
                raise ToolError('試行の採点を当て直した値が出力と違う: %s #%d' % (key, i))
    dg = BB.closing_digests(TR['trials'], SC['scored'], env)
    if canon_json(dg) != canon_json(SC['digests']):
        raise ToolError('採点の出力の数（採点の器の SHA16・採点の出力の SHA-256・番号の列の SHA-256）を計算し直した値が出力と違う')
    for key in cells:
        s_ = BB.cell_summary(C, key, TR['trials'][key], SC['scored'][key], SC['roots'][key])
        if canon_json(s_) != canon_json(SC['summaries'][key]):
            raise ToolError('升目の集計を計算し直した値が出力と違う: %s' % key)
    start = one_file(od, 'start-behavior')
    if sha256f(os.path.join(od, start)) != (S.get('start_sha256') or '').upper():
        raise ToolError('出力の置き場の起動の記録の SHA-256 が session.json の値（start_sha256）と違う')
    if load(os.path.join(od, start)).get('session') != S.get('session_id'):
        raise ToolError('起動の記録のセッションが session.json と違う（v0.2・U09）')
    return {'END': END, 'S': S, 'TR': TR, 'SC': SC, 'env': env, 'digests': dg, 'cells': cells, 'start': start, 'end': end_fn, 'outputs_sha256': got}


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
    return {'n': len(items), 'request_sha16': sha16raw(os.path.join(bd, 'request.md')), 'items_sha16': sha16f(os.path.join(bd, 'items.json'))}     # 依頼の文はバイトで（v0.2・U13）


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


def do_close(C, od, bd, rd, fail=None, out_dir=OUT_DEFAULT, allow_dry=False, now=None, rerun=False, fr_path=None):
    if fail is not None and fail not in C['behavior_pilot']['external_scoring']['fail_reasons']:
        raise ToolError('--fail の理由は閉じた一覧（%s）から選ぶ（正本 `behavior_pilot.external_scoring.fail_reasons`・v0.2・U07）' % '・'.join(C['behavior_pilot']['external_scoring']['fail_reasons']))
    R = read_outputs(C, od, allow_dry)
    items = load(os.path.join(bd, 'items.json'))['items']
    PV = load(os.path.join(bd, 'private.json'))
    if PV['outputs_sha256'] != R['outputs_sha256']:
        raise ToolError('束を作った出力と、閉じる出力が違う')
    items2, private2 = BX.bundle(C, R['TR']['trials'], families(C, R['cells']))
    if canon_json(items2) != canon_json(items) or canon_json(private2) != canon_json(PV['private']):
        raise ToolError('束を作り直した値が、束の置き場の束と違う')
    req_sha16 = sha16raw(os.path.join(bd, 'request.md'))                          # バイトで（送る器と同じ・v0.2・U13）
    if BX.request_text(C, items) != read_raw(os.path.join(bd, 'request.md')):    # 改行を訳さずに読む（v0.2・U13）
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
        if M.get('response_sha16') not in (None, sha16raw(rp)):
            raise ToolError('呼び出しの記録の返事の SHA16 が、返事のバイトの SHA16 と違う（v0.2・U13）')
        try:
            parsed = BX.parse_reply(read_raw(rp), [it['id'] for it in items])
        except (ToolError, ValueError) as e_:
            raise ToolError('返事が決まりの形でない（採点ができなかったときは --fail で理由を与える）: %s' % e_)
        ag = BX.agreement(parsed, PV['private'], R['SC']['scored'])
        ext.update(lineage=M.get('model_returned'), model_requested=M.get('model_requested'), system_fingerprint=M.get('system_fingerprint'), reply_sha16=sha16raw(rp),
                   n=ag['n'], agree=ag['agree'], share=ag['share'], by_field=ag['by_field'], rows=ag['rows'])
    else:
        ext.update(fail=fail_sentence(C, fail), reason=fail)
    iii = BB.iii_status(C, R['SC']['summaries'])
    t = now or datetime.datetime.now(JST)
    rec = collections.OrderedDict([
        ('kind', 'bprime_behavior_closed'), ('version', VERSION), ('closed_jst', t.isoformat(timespec='seconds')), ('tool_error', False),
        ('contract_sha16', sha16f(CANON)), ('session', {k: R['S'].get(k) for k in ('session_id', 'commit', 'dry', 'gpu', 'versions', 'canon_sha16', 'determinism')}),
        ('start_record', {'file': R['start'], 'sha256': sha256f(os.path.join(od, R['start']))}), ('end_record', {'file': R['end'], 'sha256': sha256f(os.path.join(od, R['end']))}),
        ('outputs_sha256', R['outputs_sha256']), ('digests', R['digests']), ('summaries', R['SC']['summaries']), ('fixed', R['TR'].get('fixed')),
        ('iii_status', {k: v for k, v in iii.items() if k != 'rate'}), ('external', ext), ('row_C', row_c(C, R, ext)),
        ('bundle', {'items_sha16': sha16f(os.path.join(bd, 'items.json')), 'private_sha16': sha16f(os.path.join(bd, 'private.json')), 'request_sha16': req_sha16}),
        ('closed_record_keys', KEYMAP), ('clause', CLAUSE)])
    return write_closed(C, rec, out_dir, rerun=rerun, fr_path=fr_path)


def do_close_tool_error(C, od, out_dir=OUT_DEFAULT, allow_dry=False, now=None, rerun=False, fr_path=None):
    ep = os.path.join(od, 'behavior-tool-error.json')
    if not os.path.exists(ep):
        raise ToolError('器の誤りの記録（behavior-tool-error.json）が無い')
    end_p = os.path.join(od, one_file(od, 'end-behavior'))
    END = load(end_p)
    if END.get('outputs_sha256', {}).get('behavior-tool-error.json') != sha256f(ep):
        raise ToolError('器の誤りの記録の SHA-256 が出力の SHA の記録と違う')
    S = load(os.path.join(od, 'session.json'))
    if S.get('dry') and not allow_dry:
        raise ToolError('DRY の出力は閉じない')
    start = one_file(od, 'start-behavior')
    if sha256f(os.path.join(od, start)) != (S.get('start_sha256') or '').upper() or load(os.path.join(od, start)).get('session') != S.get('session_id') \
            or not S.get('session_id') or END.get('session') != S.get('session_id'):
        raise ToolError('起動の記録か出力の SHA の記録が session.json と合わない（SHA・セッション・v0.2・U09）')
    t = now or datetime.datetime.now(JST)
    E = load(ep)
    ext = collections.OrderedDict([('name', C['behavior_pilot']['external_scoring']['print_name']),
                                   ('fail', fail_sentence(C, C['behavior_pilot']['external_scoring']['tool_error_reason'])),
                                   ('reason', C['behavior_pilot']['external_scoring']['tool_error_reason'])])
    rec = collections.OrderedDict([
        ('kind', 'bprime_behavior_closed'), ('version', VERSION), ('closed_jst', t.isoformat(timespec='seconds')), ('tool_error', True), ('tool_error_message', E.get('tool_error')),
        ('contract_sha16', sha16f(CANON)), ('session', {k: S.get(k) for k in ('session_id', 'commit', 'dry', 'gpu', 'versions', 'canon_sha16', 'determinism')}),
        ('start_record', {'file': start, 'sha256': sha256f(os.path.join(od, start))}),
        ('end_record', {'file': os.path.basename(end_p), 'sha256': sha256f(end_p)}), ('outputs_sha256', {'behavior-tool-error.json': sha256f(ep)}),
        ('digests', None), ('summaries', None), ('fixed', None), ('iii_status', {'status': 'tool_error', 'sentence': C['pilot']['iii_fail_sentences']['tool_error']}),
        ('external', ext), ('row_C', collections.OrderedDict([('tool_error', C['pilot']['iii_fail_sentences']['tool_error']), ('external', ext)])),     # 系統外の採点ができなかった文（v0.2・U07）
        ('closed_record_keys', KEYMAP), ('clause', CLAUSE)])
    return write_closed(C, rec, out_dir, rerun=rerun, fr_path=fr_path)


def write_closed(C, rec, out_dir, rerun=False, fr_path=None):
    os.makedirs(out_dir, exist_ok=True)
    jp = os.path.join(out_dir, 'behavior-closed-Bprime.json')
    mp = os.path.join(out_dir, 'behavior-closed-Bprime.md')
    prior = []
    if os.path.exists(jp) or os.path.exists(mp):
        if not rerun:
            raise ToolError('閉じた記録は既にある（一度だけ書く・やり直しは --rerun と台帳のやり直しの行）')
        prior = prior_for_rerun(jp, mp, out_dir, fr_path)                  # 一度目の記録を置き換えずに並べる（v0.2・U07・U09・正本 `behavior_pilot.rerun`）
    elif rerun:
        raise ToolError('--rerun なのに、やり直す前の閉じた記録が無い')
    rec['prior_closed'] = prior
    for k, path in KEYMAP.items():
        x = rec
        for part in path.split('.'):
            x = (x or {}).get(part) if isinstance(x, dict) else None
        if k not in C['behavior_pilot']['closed_record_keys'] or (x is None and not (rec['tool_error'] and path.startswith('digests'))):
            raise ToolError('閉じた記録の鍵が欠けた: %s' % k)
    write_once(jp, json.dumps(rec, ensure_ascii=False, indent=1) + NL)
    write_once(mp, render_md(C, rec, sha16f(jp)))
    return jp, mp


def prior_for_rerun(jp, mp, out_dir, fr_path):
    """やり直しの前の閉じた記録を `-prior-<セッションの頭の 8 字>` の名にバイトのまま写し、元を外す。戻り値: 新しい記録の `prior_closed`（v0.2）。
    器の誤りで閉じた記録だけ・読み取りの下見の走行がまだ無いときだけ・台帳のやり直しの行（kind behavior_rerun）がやり直しの数だけあるときだけ（正本 `behavior_pilot.rerun`）。"""
    if not (os.path.exists(jp) and os.path.exists(mp)):
        raise ToolError('やり直す前の閉じた記録の JSON と md の片方が無い')
    old = load(jp)
    if old.get('tool_error') is not True:
        raise ToolError('やり直せるのは器の誤りで閉じたときだけ（正本 `behavior_pilot.rerun`）')
    runs = os.path.join(os.path.dirname(os.path.abspath(out_dir)), 'runs')
    if os.path.isdir(runs) and any(fn.startswith('start-pilot') for fn in os.listdir(runs)):
        raise ToolError('読み取りの下見の走行が既にある（やり直しは読み取りの下見の前だけ・正本 `behavior_pilot.rerun`）')
    s8 = str((old.get('session') or {}).get('session_id') or '')[:8]
    if not re.fullmatch(r'[0-9a-f]{8}', s8):
        raise ToolError('やり直す前の閉じた記録のセッションが読めない')
    pj, pm = (os.path.join(out_dir, 'behavior-closed-Bprime-prior-%s.%s' % (s8, x)) for x in ('json', 'md'))
    prior = list(old.get('prior_closed') or []) + [collections.OrderedDict([('file', os.path.basename(pj)), ('md', os.path.basename(pm)), ('sha256', sha256f(jp)),
                                                                            ('session8', s8), ('tool_error', True), ('closed_jst', old.get('closed_jst'))])]
    n_re = P.reruns_of(load(fr_path or FR_DEFAULT).get('deviations') or []).get('behavior', 0)
    if n_re < len(prior):
        raise ToolError('台帳のやり直しの行（kind behavior_rerun）が %d で、やり直しの数 %d に足りない' % (n_re, len(prior)))
    for src, dst in ((jp, pj), (mp, pm)):
        if os.path.exists(dst):
            raise ToolError('やり直す前の閉じた記録の写しが既にある: %s' % os.path.basename(dst))
        shutil.copyfile(src, dst)
        if sha256f(src) != sha256f(dst):
            raise ToolError('写しの SHA-256 が元と違う: %s' % os.path.basename(dst))
    os.remove(jp)
    os.remove(mp)
    return prior


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
    for pr in rec.get('prior_closed') or []:
        L.append('- やり直しの前の閉じた記録（使わない・報告の頭に並べる）: `%s`（SHA-256 %s・器の誤り・閉じた時刻 %s）。' % (pr['file'], pr['sha256'], pr['closed_jst']))
    if rec['tool_error']:
        L += ['- **器の誤りで終わった**: %s。(iii) は「%s」。' % (rec.get('tool_error_message'), rec['iii_status']['sentence']),
              '- %s: %s。' % (rec['external']['name'], rec['external']['fail']), '', CLAUSE, '']
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
_TOK = {}


def _synthetic_outputs(C, od, dry=True, tamper=False, cr=False, tamper_score=False, sid='0123abcd-0000-4000-8000-000000000000'):
    """合成の行動の下見の出力（`dry_bprime_behavior` の合成の応答を升目の族に合わせて 40 件ずつ並べる・本物のトークナイザで番号にする）。"""
    import dry_bprime_behavior as DB
    from transformers import AutoTokenizer
    tok = _TOK.get('tok') or _TOK.setdefault('tok', AutoTokenizer.from_pretrained(DB.HF))     # 読み込みは一度だけ（自己検査を軽くする・v0.2）
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
            if cr:
                t['text'] = t['text'] + chr(13) + NL + '終' + chr(13)                  # 応答の中の \r\n と \r（v0.2・U13）
            sent, fam_ = BB.sent_of(key)
            T_.append(t)
            S_.append(BB.score_trial(t, fam_, sent, env))
            R_.append(BB.root_counts_trial(t, [2, 105, 2364, 107], [int(x) for x in DB.LEDGER['cells_main'][key]['set_ids']], DB.LEDGER['prefix_ids'], strings, window, env['parser_mod']))
        trials[key], scored[key], roots[key] = T_, S_, R_
        summaries[key] = BB.cell_summary(C, key, T_, S_, R_)
    if tamper_score:                                                      # 採点だけを書き換え、数と集計は書き換えた採点から計算し直す（当て直しだけが捕まえる・v0.2・U26）
        k0 = next(k for k in scored if any(x['score'] is not None for x in scored[k]))
        j0 = next(j for j, x in enumerate(scored[k0]) if x['score'] is not None)
        scored[k0][j0] = dict(scored[k0][j0], score=dict(scored[k0][j0]['score'], choice='zz'))
        summaries[k0] = BB.cell_summary(C, k0, trials[k0], scored[k0], roots[k0])
    digests = BB.closing_digests(trials, scored, env)
    os.makedirs(od, exist_ok=True)

    def wj(fn, o):
        with open(os.path.join(od, fn), 'w', encoding='utf-8', newline=NL) as fh:
            fh.write(json.dumps(o, ensure_ascii=False, indent=1) + NL)
    wj('behavior-trials.json', {'trials': trials, 'calls': {}, 'fixed': {'processors': ['合成'], 'do_sample': True}, 'clause': CLAUSE})
    wj('behavior-scored.json', {'scored': scored, 'roots': roots, 'summaries': summaries, 'digests': digests, 'clause': CLAUSE})
    st_fn, en_fn = 'start-behavior-%s.json' % sid[:8], 'end-behavior-%s.json' % sid[:8]
    wj(st_fn, {'kind': 'bprime_start_record', 'phase': 'behavior', 'session': sid})
    wj('session.json', {'kind': 'bprime_colab_behavior', 'dry': dry, 'commit': 'dry', 'gpu': 'dry', 'versions': {'transformers': '5.16.1', 'tokenizers': 'x'}, 'canon_sha16': sha16f(CANON),
                        'start_record': st_fn, 'start_sha256': sha256f(os.path.join(od, st_fn)), 'session_id': sid})
    if tamper:
        summaries[list(summaries)[0]]['catastrophe'] += 1
        wj('behavior-scored.json', {'scored': scored, 'roots': roots, 'summaries': summaries, 'digests': digests, 'clause': CLAUSE})
    wj(en_fn, {'kind': 'bprime_end_record', 'phase': 'behavior', 'session': sid,
               'outputs_sha256': {fn: sha256f(os.path.join(od, fn)) for fn in ('behavior-trials.json', 'behavior-scored.json')}})
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
        # 起動の記録の写しが session の SHA と違えば止まる（K19）
        od5 = os.path.join(td, 'out5')
        _synthetic_outputs(C, od5)
        _wt(os.path.join(od5, 'start-behavior-0123abcd.json'), '{"kind": "bprime_start_record", "phase": "behavior", "x": 1}')
        try:
            do_bundle(C, od5, os.path.join(td, 'b5'), allow_dry=True)
            ok.append(('起動の記録の写しの差し替えで止まる', False))
        except ToolError:
            ok.append(('起動の記録の写しの差し替えで止まる', True))
        # 器の誤りで閉じる
        od4 = os.path.join(td, 'out4')
        os.makedirs(od4)
        _wt(os.path.join(od4, 'behavior-tool-error.json'), json.dumps({'tool_error': '合成の誤り'}, ensure_ascii=False))
        sid4 = 'fedc9876-0000-4000-8000-000000000000'
        _wt(os.path.join(od4, 'start-behavior-fedc9876.json'), json.dumps({'kind': 'bprime_start_record', 'phase': 'behavior', 'session': sid4}))
        _wt(os.path.join(od4, 'session.json'), json.dumps({'kind': 'bprime_colab_behavior', 'dry': True, 'session_id': sid4,
                                                         'start_sha256': sha256f(os.path.join(od4, 'start-behavior-fedc9876.json'))}))
        _wt(os.path.join(od4, 'end-behavior-fedc9876.json'), json.dumps({'kind': 'bprime_end_record', 'phase': 'behavior', 'session': sid4,
                                                                         'outputs_sha256': {'behavior-tool-error.json': sha256f(os.path.join(od4, 'behavior-tool-error.json'))}}))
        recs = os.path.join(td, 'recs')
        closed4 = os.path.join(recs, 'behavior')
        jp4, mp4 = do_close_tool_error(C, od4, out_dir=closed4, allow_dry=True, now=t0)
        R4 = load(jp4)
        ok.append(('器の誤りで閉じた記録', R4['tool_error'] is True and R4['iii_status']['status'] == 'tool_error' and '較正できなかった' in open(mp4, encoding='utf-8').read()))
        ok.append(('正本 v5 の理由の一覧と器の定数が同じ', list(FAIL_REASONS) == list(C['behavior_pilot']['external_scoring']['fail_reasons'])
                   and TOOL_ERROR_REASON == C['behavior_pilot']['external_scoring']['tool_error_reason']))
        ok.append(('器の誤りで閉じた記録に系統外の採点ができなかった文（理由つき・転記行 C にも）', R4['external']['fail'] == '系統外の模型による採点ができなかった（%s）' % TOOL_ERROR_REASON
                   and R4['row_C']['external'] == R4['external'] and TOOL_ERROR_REASON in open(mp4, encoding='utf-8').read()))
        # やり直しの道（v0.2・U07・U09・正本 `behavior_pilot.rerun`）
        od7, b7d = od, bd                                                   # 一つ目の合成の出力と束を使い回す（自己検査の計算を軽くする）
        fr0, fr1 = os.path.join(td, 'fr0.json'), os.path.join(td, 'fr1.json')
        _wt(fr0, json.dumps({'deviations': [{'kind': 'pilot_rerun'}]}))
        _wt(fr1, json.dumps({'deviations': [{'kind': 'behavior_rerun'}]}))
        for nm_, kw_ in (('やり直しの印が無ければ閉じた記録を書き換えない', {}), ('台帳にやり直しの行が無ければ止まる', {'rerun': True, 'fr_path': fr0})):
            try:
                do_close(C, od7, b7d, None, fail='呼び出しの失敗', out_dir=closed4, allow_dry=True, now=t0, **kw_)
                ok.append((nm_, False))
            except ToolError:
                ok.append((nm_, True))
        old_sha = sha256f(jp4)
        jp7, mp7 = do_close(C, od7, b7d, None, fail='呼び出しの失敗', out_dir=closed4, allow_dry=True, now=t0, rerun=True, fr_path=fr1)
        R7 = load(jp7)
        pj7 = os.path.join(closed4, 'behavior-closed-Bprime-prior-fedc9876.json')
        ok.append(('やり直しで一度目の記録をバイトのまま並べ、新しい記録に並べる', os.path.exists(pj7) and sha256f(pj7) == old_sha and R7['prior_closed'][0]['sha256'] == old_sha
                   and R7['tool_error'] is False and R7['start_record']['file'] == 'start-behavior-0123abcd.json' and 'やり直しの前の閉じた記録' in open(mp7, encoding='utf-8').read()))
        try:
            do_close(C, od7, b7d, None, fail='呼び出しの失敗', out_dir=closed4, allow_dry=True, now=t0, rerun=True, fr_path=fr1)
            ok.append(('器の誤りでない閉じた記録はやり直さない', False))
        except ToolError:
            ok.append(('器の誤りでない閉じた記録はやり直さない', True))
        recs8 = os.path.join(td, 'recs8')
        do_close_tool_error(C, od4, out_dir=os.path.join(recs8, 'behavior'), allow_dry=True, now=t0)
        os.makedirs(os.path.join(recs8, 'runs'))
        _wt(os.path.join(recs8, 'runs', 'start-pilot-11112222.json'), '{}')
        try:
            do_close(C, od7, b7d, None, fail='呼び出しの失敗', out_dir=os.path.join(recs8, 'behavior'), allow_dry=True, now=t0, rerun=True, fr_path=fr1)
            ok.append(('読み取りの下見の走行の後はやり直さない', False))
        except ToolError:
            ok.append(('読み取りの下見の走行の後はやり直さない', True))
        try:
            do_close(C, od7, b7d, None, fail='合成の理由', out_dir=os.path.join(td, 'closed9'), allow_dry=True, now=t0)
            ok.append(('--fail の理由は閉じた一覧から', False))
        except ToolError:
            ok.append(('--fail の理由は閉じた一覧から', True))
        # 採点の書き換え（数と集計は書き換えた採点から計算し直した形）は当て直しで止まる（v0.2・U26）
        od10 = os.path.join(td, 'out10')
        _synthetic_outputs(C, od10, tamper_score=True)
        try:
            do_bundle(C, od10, os.path.join(td, 'b10'), allow_dry=True)
            ok.append(('採点の書き換えは当て直しで止まる', False))
        except ToolError as e_:
            ok.append(('採点の書き換えは当て直しで止まる', '当て直した' in str(e_)))
        # 応答の中の \r と、\r\n の返事でも閉じる（改行を訳さずに読む・SHA はバイト・v0.2・U13）
        od11, bd11, rd11 = (os.path.join(td, x) for x in ('out11', 'b11', 'r11'))
        sc11 = _synthetic_outputs(C, od11, cr=True)
        b11 = do_bundle(C, od11, bd11, allow_dry=True)
        req11 = read_raw(os.path.join(bd11, 'request.md'))
        items11 = load(os.path.join(bd11, 'items.json'))['items']
        PV11 = load(os.path.join(bd11, 'private.json'))['private']
        lines11 = []
        for it in items11:
            key, ti = PV11[it['id']]
            s = sc11[key][ti]['score']
            lines11.append(json.dumps({'id': it['id'], 'format': '書式外' if (s is None or s['format_fail']) else 'ok', 'choice': None if s is None else s['choice'],
                                       'catastrophe': None if s is None else s['catastrophe']}, ensure_ascii=False))
        os.makedirs(rd11)
        raw11 = (chr(13) + NL).join(lines11) + chr(13) + NL
        with open(os.path.join(rd11, 'response.md'), 'wb') as fh:
            fh.write(raw11.encode('utf-8'))
        _wt(os.path.join(rd11, 'meta.json'), json.dumps({'request_sha16': b11['request_sha16'], 'response_sha16': hashlib.sha256(raw11.encode('utf-8')).hexdigest().upper()[:16]}))
        jp11, _ = do_close(C, od11, bd11, rd11, out_dir=os.path.join(td, 'closed11'), allow_dry=True, now=t0)
        R11 = load(jp11)
        ok.append(('応答の \\r と返事の \\r\\n で閉じ、SHA はバイト', chr(13) in req11 and R11['external']['agree'] == R11['external']['n']
                   and R11['external']['reply_sha16'] == hashlib.sha256(raw11.encode('utf-8')).hexdigest().upper()[:16]))
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
    ap.add_argument('--rerun', action='store_true')
    ap.add_argument('--freeze', default=FR_DEFAULT)
    a = ap.parse_args()
    C = load(CANON)
    if a.stage == 'bundle':
        print('[close_behavior_Bprime] 束: %s' % do_bundle(C, a.paths[0], a.paths[1], a.allow_dry))
    elif a.stage == 'close':
        jp, mp = do_close(C, a.paths[0], a.paths[1], a.paths[2] if len(a.paths) > 2 else None, fail=a.fail, out_dir=a.out, allow_dry=a.allow_dry, rerun=a.rerun, fr_path=a.freeze)
        print('[close_behavior_Bprime] 閉じた記録: %s（SHA16 %s）・%s' % (jp, sha16f(jp), mp))
    else:
        jp, mp = do_close_tool_error(C, a.paths[0], out_dir=a.out, allow_dry=a.allow_dry, rerun=a.rerun, fr_path=a.freeze)
        print('[close_behavior_Bprime] 器の誤りで閉じた記録: %s（SHA16 %s）' % (jp, sha16f(jp)))


if __name__ == '__main__':
    main()
