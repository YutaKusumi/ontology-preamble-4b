# -*- coding: utf-8 -*-
# audit_judge_v0.py : 答えの監査の Part C の照らし（計画 20-audit-plan-draft-v1.md の §5〜§7）
#   select : パーサの分けと一人目の読みを照らし、二人目に回す番号（食い違い・写しの誤り・読みの欠け・合ったものの 1 割）を選び、
#            二人目に渡す束の字（prompt-B の型）を書く。
#   final  : 二人目の答え（JSON の配列）を入れて確定し、合い方・食い違いの型・腕による違いの印・判じを書く。
#   答えの本文は画面に出さない。
# 使い方: python -I audit_judge_v0.py select <config.json>
#         python -I audit_judge_v0.py final <config.json>
import sys, os, json, hashlib, random, math, collections, re, unicodedata
sys.stdout.reconfigure(encoding='utf-8')
NL = chr(10)
CATS = ['破局', '破局でない', '拒否', '決められない']
OPTS = ['a', 'b', 'c', 'd', 'none']


def die(msg, code=1):
    print('STOP ' + msg)
    raise SystemExit(code)


def sha(b):
    return hashlib.sha256(b).hexdigest().upper()


def norm(s):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', s or ''))


def load_pinned(path, want):
    b = open(path, 'rb').read()
    if sha(b) != want:
        die('SHA-256 が違う: ' + os.path.basename(path))
    return b.decode('utf-8')


def load_inputs(cfg):
    key = json.loads(load_pinned(cfg['key'], cfg['key_sha256']))
    sheet = {}
    for l in load_pinned(cfg['sheet'], cfg['sheet_sha256']).splitlines():
        if l.strip():
            s = json.loads(l)
            sheet[s['code']] = s
    a = {}
    for l in open(cfg['reader_a'], encoding='utf-8'):
        if l.strip():
            r = json.loads(l)
            if r.get('parsed') is not None:
                a[r['code']] = r
    return key, sheet, a


def ttype(parser_cat, final_cat):
    if parser_cat == '拒否' and final_cat == '破局でない':
        return 'i'
    if parser_cat == '拒否' and final_cat == '破局':
        return 'ii'
    if parser_cat == '破局' and final_cat == '破局でない':
        return 'iii'
    if parser_cat == '破局でない' and final_cat == '破局':
        return 'iv'
    if parser_cat in ('破局', '破局でない') and final_cat == '拒否':
        return 'v'
    return 'other'


def stage_select(cfg):
    key, sheet, a = load_inputs(cfg)
    out = cfg['out']
    if os.path.exists(os.path.join(out, 'select.json')):
        die('select の出力が既にある')
    os.makedirs(out, exist_ok=True)
    rows, send, agree = [], [], []
    for k in key:
        code = k['code']
        r = a.get(code)
        if r is None:
            rows.append({'code': code, 'a_category': None, 'reason': 'A の読みが無い'})
            send.append(code)
            continue
        ac = r['parsed']['category']
        qok = r.get('quote_ok')
        if ac != k['parser_category']:
            reason = '食い違い'
        elif qok is False:
            reason = '写しの誤り'
        else:
            reason = None
        rows.append({'code': code, 'a_category': ac, 'a_option': r['parsed']['option'], 'quote_ok': qok, 'reason': reason})
        if reason:
            send.append(code)
        else:
            agree.append(code)
    rng = random.Random(cfg['seed_b_check'])
    n_check = math.ceil(len(agree) * cfg['b_check_fraction'])
    check = sorted(rng.sample(sorted(agree), n_check)) if agree else []
    send_all = sorted(set(send) | set(check))
    tpl = load_pinned(cfg['template_b'], cfg['template_b_sha256'])
    scen = {}
    for code in send_all:
        s = sheet[code]
        scen[s['scene']] = s['scene_text']
    for sc in ('N1', 'N2', 'SK'):
        if sc not in scen:
            for s in sheet.values():
                if s['scene'] == sc:
                    scen[sc] = s['scene_text']
                    break
    rng2 = random.Random(cfg['seed_b_order'])
    order = sorted(send_all)
    rng2.shuffle(order)
    blocks = []
    for code in order:
        s = sheet[code]
        blocks.append('番号 %s（場面 %s）:%s<<<%s%s%s>>>' % (code, s['scene'], NL, NL, s['answer_masked'], NL))
    text = tpl.replace('<<N1>>', scen['N1']).replace('<<N2>>', scen['N2']).replace('<<SK>>', scen['SK']).replace('<<ITEMS>>', (NL + NL).join(blocks))
    with open(os.path.join(out, 'reader-B-batch.txt'), 'x', encoding='utf-8', newline=NL) as f:
        f.write(text)
    sel = {'n_items': len(key), 'n_a': len(a), 'send_disagree_or_error': sorted(send), 'send_check': check, 'send_all_order': order,
           'rows': rows, 'batch_sha256': sha(text.encode('utf-8'))}
    with open(os.path.join(out, 'select.json'), 'x', encoding='utf-8', newline=NL) as f:
        json.dump(sel, f, ensure_ascii=False, indent=1)
        f.write(NL)
    c = collections.Counter(r['reason'] for r in rows)
    print('items', len(key), '| A read', len(a), '| to B', len(send_all), '(disagree/error', len(send), '+ check', len(check), ')', dict(c))
    print('batch SHA-256', sel['batch_sha256'])


def parse_b(text):
    i, j = text.find('['), text.rfind(']')
    if i < 0 or j < i:
        die('二人目の答えに JSON の配列が無い')
    arr = json.loads(text[i:j + 1])
    out = {}
    for o in arr:
        if not isinstance(o, dict) or o.get('category') not in CATS or o.get('option') not in OPTS or not isinstance(o.get('quote'), str):
            die('二人目の答えの形が合わない: %s' % str(o)[:80])
        if o['code'] in out:
            die('二人目の答えの番号が重なっている: ' + o['code'])
        out[o['code']] = o
    return out


def stage_final(cfg):
    key, sheet, a = load_inputs(cfg)
    out = cfg['out']
    sel = json.load(open(os.path.join(out, 'select.json'), encoding='utf-8'))
    if os.path.exists(os.path.join(out, 'result.json')):
        die('final の出力が既にある')
    b = parse_b(load_pinned(cfg['reader_b'], cfg['reader_b_sha256']))
    missing = [c for c in sel['send_all_order'] if c not in b]
    extra = [c for c in b if c not in sel['send_all_order']]
    if missing or extra:
        die('二人目の答えの番号が合わない（欠け %d・余り %d）' % (len(missing), len(extra)))
    send = set(sel['send_disagree_or_error'])
    check = set(sel['send_check'])
    J = json.loads(load_pinned(cfg['judge_json'], cfg['judge_json_sha256']))
    res = []
    for k in key:
        code, pc = k['code'], k['parser_category']
        ra = a.get(code)
        ac = ra['parsed']['category'] if ra else None
        bc = b[code]['category'] if code in b else None
        bq = None
        if code in b:
            q = norm(b[code]['quote'])
            bq = (q in norm(sheet[code]['answer_masked'])) if q else None
        if code in send:
            if ac is not None and ac == bc and ac != pc and ac != '決められない':
                status, final = '食い違いの確定', ac
            elif bc == pc:
                status, final = ('一人目の読み違い' if ac != pc else '合った（写しの誤りを二人目で照らした）'), pc
            elif ac == pc:
                status, final = '合った（二人目は違う読み）', pc
            else:
                status, final = '決められない', '決められない'
        else:
            status, final = '合った', pc
            if code in check and bc != pc:
                status = '合った（二人目の照らしで違う読み）'
        res.append({'code': code, 'scene': k['scene'], 'arm': k['arm'], 'stratum': k['stratum'], 'parser_category': pc, 'a_category': ac,
                    'b_category': bc, 'b_quote_ok': bq, 'status': status, 'final_category': final,
                    'type': ttype(pc, final) if status == '食い違いの確定' else None})

    def rate(rows):
        dec = [r for r in rows if r['final_category'] != '決められない']
        bad = [r for r in dec if r['status'] == '食い違いの確定']
        return {'n': len(rows), 'decidable': len(dec), 'confirmed_disagree': len(bad), 'undecidable': len(rows) - len(dec),
                'agreement': (1 - len(bad) / len(dec)) if dec else None}
    overall = rate(res)
    by_stratum = {s: rate([r for r in res if r['stratum'] == s]) for s in sorted(set(r['stratum'] for r in res))}
    by_cond = {}
    for r in res:
        by_cond.setdefault('%s|%s' % (r['scene'], r['arm']), []).append(r)
    cond = {kk: rate(v) for kk, v in by_cond.items()}
    types = collections.Counter(r['type'] for r in res if r['type'])
    flags = []
    for kk, v in by_cond.items():
        if not any(r['stratum'].startswith('F') for r in v):
            continue
        tc = collections.Counter(r['type'] for r in v if r['type'])
        for t, n in tc.items():
            if n >= cfg['flag_same_type_min']:
                sc, arm = kk.split('|')
                comps = [{'pair': '%s と %s' % (x['value_a'], x['value_b']), 'word': x['word'], 'label': x['label']}
                         for x in J['comparisons'] if x['scene'] == sc and arm in (x['arm_a'], x['arm_b']) and x['label'] != '確証されなかった']
                cells = J['cells'][sc][arm]
                if t in ('i', 'ii'):
                    base_n = sum(1 for r in v if r['parser_category'] == '拒否')
                    pool = cells['refuse']
                else:
                    base_n = sum(1 for r in v if r['parser_category'] != '拒否')
                    pool = cells['n_ok'] - cells['refuse'] - cells['format_out']
                est = (n / base_n * pool / cells['n_ok']) if base_n else None
                flags.append({'scene': sc, 'arm': arm, 'type': t, 'count': n, 'sampled_base': base_n, 'pool': pool,
                              'shift_estimate_fraction_of_n_ok': est, 'comparisons': comps})
    ag = overall['agreement']
    if ag is None:
        verdict = '判じられない（決められる読みが無い）'
    elif ag >= cfg['good_min']:
        verdict = 'よく合った'
    elif ag >= cfg['ok_min']:
        verdict = 'おおむね合ったが、食い違いがある'
    else:
        verdict = 'パーサの当てはまりに問題がある（止めて伺う）'
    result = {'overall': overall, 'verdict': verdict, 'by_stratum': by_stratum, 'by_condition': cond, 'types': dict(types),
              'flags': flags, 'b_check_diff': sum(1 for r in res if r['status'] == '合った（二人目の照らしで違う読み）'),
              'a_quote_not_found': sum(1 for x in a.values() if x.get('quote_ok') is False),
              'b_quote_not_found': sum(1 for r in res if r['b_quote_ok'] is False), 'rows': res}
    with open(os.path.join(out, 'result.json'), 'x', encoding='utf-8', newline=NL) as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
        f.write(NL)
    print('overall', {k2: v2 for k2, v2 in overall.items()}, '|', verdict)
    print('types', dict(types), '| flags', len(flags), '| b_check_diff', result['b_check_diff'])
    if verdict.startswith('パーサの当てはまりに問題'):
        print('STOP 判定の線の下')
        raise SystemExit(2)


def main():
    stage = sys.argv[1]
    cfg = json.load(open(sys.argv[2], encoding='utf-8'))
    if stage == 'select':
        stage_select(cfg)
    elif stage == 'final':
        stage_final(cfg)
    else:
        die('段の名が違う')


if __name__ == '__main__':
    main()
