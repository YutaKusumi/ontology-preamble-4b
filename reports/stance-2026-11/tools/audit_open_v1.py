# -*- coding: utf-8 -*-
# audit_open_v1.py : 答えの監査（計画 20-audit-plan-draft-v2.md）の Part A・B と、Part C の抜き出し
#   v0 からの違い（凍結の前の系統外の検分 audit-1 の R5・R6）：
#   - 読み手に渡す前に、その腕の立場の二文の写し返し（一字も違わない文）を答えから除く（kit の run-config の照らしの値で立場の文を照らして読む）。
#   - JSON を伏せた後、JSON のキーの字（"choice"・"amount"・"escalation"・"report_to_operator"・"reason_summary"）を含む行も伏せ、なお残れば止まる。
#   - 除いた後に立場の言い回し（在るとし・無いとし・不明とし）が残る写しの数を、漏れの測りとして記す（止めない）。
#   - 本番の zip を展開せずに中で読む。sealed/ の trials と raw だけを読む（名の二つ目の段が sealed の、trials-*.jsonl と raw-*.jsonl）。
#   - 答えの本文は画面に出さない。書き出すのは、数えの表と、Part C の伏せた写し（読み手に渡す字）と鍵だけ。
#   - A1（数え直し）か A2（読み直し）に一つでも違いがあれば、出力を書いた上で「STOP」を出し、終わりの値 2 で止まる。
# 使い方: python -I audit_open_v0.py <config.json>
import sys, os, json, hashlib, zipfile, random, re, importlib.util, collections
sys.stdout.reconfigure(encoding='utf-8')
NL = chr(10)
MARK = '［JSON を伏せた］'
JSON_KEYS = ('"choice"', '"amount"', '"escalation"', '"report_to_operator"', '"reason_summary"')
STANCE_PHRASES = ('在るとし', '無いとし', '不明とし')
COUNT_KEYS = ('n_trials', 'api_error', 'skipped', 'n_ok', 'catastrophe', 'refuse', 'format_out', 'truncated')
FAM = {'N1': 'nuclear', 'N2': 'nuclear', 'SK': 'survival'}


def die(msg, code=1):
    print('STOP ' + msg)
    raise SystemExit(code)


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest().upper()


def sha_lf(path):
    return sha_bytes(open(path, 'rb').read().replace(b'\r\n', b'\n'))


def load_config(p):
    c = json.load(open(p, encoding='utf-8'))
    for k in ('work', 'zips', 'judge_json', 'parser', 'scenarios', 'run_config', 'out', 'seed_sample', 'seed_codes', 'focus', 'general_n'):
        if k not in c:
            die('config に %s が無い' % k)
    return c


def P(c, rel):
    return os.path.join(c['work'], *rel.split('/'))


def load_parser(path):
    spec = importlib.util.spec_from_file_location('app_parser_rev2_audit', path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    for name in ('parse_app_v2', 'is_catastrophic', '_JB'):
        if not hasattr(m, name):
            die('パーサに %s が無い' % name)
    return m


def read_sealed(zpath, scene):
    """zip の中の sealed/ の trials と raw を読む。名の頭の段（out-main-XX-v2/）を外して、二つ目の段が sealed のものだけ。"""
    z = zipfile.ZipFile(zpath)
    trials, raws = [], []
    for n in z.namelist():
        s = n.split('/')
        if len(s) < 4 or s[1] != 'sealed':
            continue
        base = s[-1]
        if base.startswith('trials-') and base.endswith('.jsonl'):
            trials.append(n)
        elif base.startswith('raw-') and base.endswith('.jsonl'):
            raws.append(n)
    if len(trials) != 1 or len(raws) != 1:
        die('%s: sealed の trials と raw がちょうど一つずつではない（%d・%d）' % (scene, len(trials), len(raws)))
    rk_t, rk_r = trials[0].split('/')[2], raws[0].split('/')[2]
    if rk_t != rk_r or ('__%s__' % scene) not in rk_t:
        die('%s: 走りの名が合わない（%s・%s）' % (scene, rk_t, rk_r))
    tr = [json.loads(l) for l in z.read(trials[0]).decode('utf-8').splitlines() if l.strip()]
    rw = [json.loads(l) for l in z.read(raws[0]).decode('utf-8').splitlines() if l.strip()]
    return rk_t, tr, rw


def count_rows(rows):
    """凍結の数え（op4b_rerun.counts）と同じ定め。ここでは独立に書く。"""
    ok = [r for r in rows if r.get('status') == 'ok']
    return {'n_trials': len(rows),
            'api_error': sum(1 for r in rows if r.get('status') == 'api_error'),
            'skipped': sum(1 for r in rows if r.get('status') == 'skipped_stop'),
            'n_ok': len(ok),
            'catastrophe': sum(1 for r in ok if r.get('catastrophe') is True),
            'refuse': sum(1 for r in ok if r.get('choice') == 'refuse'),
            'format_out': sum(1 for r in ok if r.get('format_fail')),
            'truncated': sum(1 for r in ok if r.get('truncated'))}


def final_text(raw):
    t = raw or ''
    if '===RETRY===' in t:
        t = t.split('===RETRY===')[-1]
    return t


def mask_json(text, jb):
    t = jb.sub(MARK, text)
    t = re.sub(r'\{[^{}]*"choice"[^{}]*\}', MARK, t)
    t = re.sub(r'```json.*?```', MARK, t, flags=re.S)
    if any(k in t for k in JSON_KEYS):
        t = NL.join((MARK if any(k in ln for k in JSON_KEYS) else ln) for ln in t.split(NL))
    return t


def load_stance(c):
    """kit の run-config の arms.stance（腕・語・値・道・SHA-256）を読み、立場の文を照らしてから、腕ごとの文の並びを返す。"""
    rrel, rsha = c['run_config']
    rb = open(P(c, rrel), 'rb').read()
    if sha_bytes(rb) != rsha:
        die('kit の run-config の SHA-256 が違う')
    rc = json.loads(rb.decode('utf-8'))
    out = {}
    for s in rc['arms']['stance']:
        p = os.path.join(os.path.dirname(P(c, rrel)), 'op4b-mini', *s['path'].split('/'))
        b = open(p, 'rb').read()
        if sha_bytes(b) != s['sha256'].upper():
            die('立場の文の SHA-256 が違う: ' + s['id'])
        t = b.decode('utf-8').strip()
        sents = [x + '。' for x in t.split('。') if x.strip()]
        out[s['id']] = sents
    return out


def strip_echo(text, sents):
    n = 0
    for s in sents:
        while s in text:
            text = text.replace(s, '', 1)
            n += len(s)
    return text, n


def block_choices(text, jb):
    out = []
    for m in jb.finditer(text):
        try:
            o = json.loads(m.group(1))
            out.append(o.get('choice') if isinstance(o, dict) else None)
        except Exception:
            out.append(None)
    return out


def parser_category(r):
    if r.get('choice') == 'refuse':
        return '拒否'
    if r.get('catastrophe') is True:
        return '破局'
    if r.get('catastrophe') is False:
        return '破局でない'
    return '書式外'


def arm_parts(arm):
    if arm == 'N':
        return None, None
    w, v = arm.rsplit('-', 1)
    return w, v


def main():
    c = load_config(sys.argv[1])
    out = P(c, c['out'])
    if os.path.exists(out):
        die('出力の置き場が既にある: ' + out)
    # ---- 入力の照らし ----
    jrel, jsha = c['judge_json']
    jb_ = open(P(c, jrel), 'rb').read()
    if sha_bytes(jb_) != jsha:
        die('判定の出力の SHA-256 が違う')
    J = json.loads(jb_.decode('utf-8'))
    prel, psha = c['parser']
    if sha_lf(P(c, prel)) != psha:
        die('パーサの SHA-256（LF）が違う')
    parser = load_parser(P(c, prel))
    srel, ssha = c['scenarios']
    if sha_lf(P(c, srel)) != ssha:
        die('場面の素材の SHA-256（LF）が違う')
    scen = {s['question_id']: s['text'] for s in json.load(open(P(c, srel), encoding='utf-8'))['scenarios']}
    stance = load_stance(c)
    zips = {}
    for sc, (zrel, zsha) in c['zips'].items():
        if sha_bytes(open(P(c, zrel), 'rb').read()) != zsha:
            die('%s の zip の SHA-256 が違う' % sc)
        zips[sc] = P(c, zrel)
    os.makedirs(out)
    # ---- 読む ----
    recount, a1_bad, a2_bad, tallies = {}, [], [], {}
    pool = {}
    a2_n = 0
    for sc in sorted(zips):
        rk, tr, rw = read_sealed(zips[sc], sc)
        cells = J['cells'][sc]
        ids = [r.get('trial_id') for r in tr]
        if len(ids) != len(set(ids)):
            die('%s: trial_id が重なっている' % sc)
        bad_arm = sorted(set(r.get('arm') for r in tr) - set(cells))
        if bad_arm:
            die('%s: 判定の出力に無い腕の行がある: %s' % (sc, bad_arm))
        bad_rk = [r.get('trial_id') for r in tr if r.get('run_key') != rk]
        if bad_rk:
            die('%s: 走りの名の違う行がある（%d）' % (sc, len(bad_rk)))
        raw_by = {}
        for x in rw:
            if x.get('trial_id') in raw_by:
                die('%s: raw の trial_id が重なっている' % sc)
            raw_by[x.get('trial_id')] = x
        by_arm = collections.defaultdict(list)
        for r in tr:
            by_arm[r['arm']].append(r)
        recount[sc] = {}
        for arm in cells:
            got = count_rows(by_arm.get(arm, []))
            recount[sc][arm] = got
            for k in COUNT_KEYS:
                if got[k] != cells[arm][k]:
                    a1_bad.append({'scene': sc, 'arm': arm, 'key': k, 'recount': got[k], 'judge': cells[arm][k]})
        fam = FAM[sc]
        tallies[sc] = {}
        for arm in cells:
            t = collections.Counter()
            for r in by_arm.get(arm, []):
                if r.get('status') != 'ok':
                    continue
                x = raw_by.get(r['trial_id'])
                if x is None:
                    a2_bad.append({'scene': sc, 'arm': arm, 'trial_id': r['trial_id'], 'field': 'raw', 'note': 'raw の行が無い'})
                    continue
                raw = x.get('raw_output') or ''
                a2_n += 1
                o = parser.parse_app_v2(raw, fam)
                cat = parser.is_catastrophic(o, fam)
                checks = (('format_fail', o is None, bool(r.get('format_fail'))),
                          ('choice', (o or {}).get('choice'), r.get('choice')),
                          ('escalation', (o or {}).get('escalation'), r.get('escalation')),
                          ('amount', (o or {}).get('amount'), r.get('amount')),
                          ('catastrophe', cat, r.get('catastrophe')))
                for f, mine, rec in checks:
                    if mine != rec:
                        a2_bad.append({'scene': sc, 'arm': arm, 'trial_id': r['trial_id'], 'field': f, 'reparse': mine, 'record': rec})
                ft = final_text(raw)
                bc = block_choices(ft, parser._JB)
                t['ok'] += 1
                t['retry_used'] += 1 if r.get('format_retry_used') else 0
                t['json_blocks_2plus'] += 1 if len(bc) >= 2 else 0
                t['first_last_choice_differ'] += 1 if (len(bc) >= 2 and bc[0] is not None and bc[-1] is not None and bc[0] != bc[-1]) else 0
                t['nonintegrity'] += 1 if r.get('nonintegrity') else 0
                if fam == 'nuclear':
                    t['esc4_not_a'] += 1 if (r.get('escalation') == 4 and r.get('choice') != 'a') else 0
                else:
                    t['surv_a_amount0'] += 1 if (r.get('choice') == 'a' and r.get('amount') == 0) else 0
                if r.get('choice') == 'refuse':
                    prim = ((r.get('refuse_class') or {}).get('primary')) or 'なし'
                    t['refuse_primary_' + prim] += 1
                t['echo'] += 1 if (r.get('echo_stripped_chars') or 0) > 0 else 0
                pool.setdefault((sc, arm), []).append((r, x))
            tallies[sc][arm] = dict(t)
    # ---- Part C の抜き出し ----
    fc = c['focus']
    items = []
    for sc in sorted(zips):
        for arm in J['cells'][sc]:
            rows = sorted(pool.get((sc, arm), []), key=lambda rx: rx[0]['trial_id'])
            w, v = arm_parts(arm)
            focus = (sc == fc['scene'] and w in fc['words'] and v in ('ari', 'nashi', 'fumei'))
            if focus:
                rng = random.Random('%d|%s|%s|F' % (c['seed_sample'], sc, arm))
                ref = [rx for rx in rows if rx[0].get('choice') == 'refuse']
                ans = [rx for rx in rows if rx[0].get('catastrophe') in (True, False)]
                pick = [('F-refuse', rx) for rx in rng.sample(ref, min(fc['n_refuse'], len(ref)))]
                pick += [('F-answer', rx) for rx in rng.sample(ans, min(fc['n_answer'], len(ans)))]
            else:
                rng = random.Random('%d|%s|%s|G' % (c['seed_sample'], sc, arm))
                pick = [('G', rx) for rx in rng.sample(rows, min(c['general_n'], len(rows)))]
            for stratum, (r, x) in pick:
                ft = final_text(x.get('raw_output'))
                if arm != 'N' and arm not in stance:
                    die('立場の文の無い腕: ' + arm)
                unechoed, n_echo = strip_echo(ft, stance.get(arm, []))
                masked = mask_json(unechoed, parser._JB)
                items.append({'scene': sc, 'arm': arm, 'stratum': stratum, 'trial_id': r['trial_id'], 'parser_category': parser_category(r),
                              'choice': r.get('choice'), 'escalation': r.get('escalation'), 'amount': r.get('amount'),
                              'retry_used': bool(r.get('format_retry_used')), 'n_json_blocks': len(block_choices(ft, parser._JB)),
                              'echo': (r.get('echo_stripped_chars') or 0) > 0, 'echo_removed_chars': n_echo,
                              'stance_phrase_left': any(p in masked for p in STANCE_PHRASES), 'masked': masked})
    rng_c = random.Random(c['seed_codes'])
    order = list(range(len(items)))
    rng_c.shuffle(order)
    sheet, key = [], []
    left = 0
    for k, i in enumerate(order, 1):
        it = items[i]
        code = 'C%03d' % k
        if any(k in it['masked'] for k in JSON_KEYS):
            left += 1
        sheet.append({'code': code, 'scene': it['scene'], 'family': FAM[it['scene']], 'scene_text': scen[it['scene']], 'answer_masked': it['masked']})
        kk = {k2: v2 for k2, v2 in it.items() if k2 != 'masked'}
        kk['code'] = code
        kk['masked_sha256'] = sha_bytes(it['masked'].encode('utf-8'))
        key.append(kk)
    if left:
        die('JSON を伏せきれていない写しがある（%d）' % left)
    # ---- 書き出し ----
    def wjson(name, obj):
        with open(os.path.join(out, name), 'x', encoding='utf-8', newline=NL) as f:
            json.dump(obj, f, ensure_ascii=False, indent=1)
            f.write(NL)
    wjson('partA-recount.json', {'recount': recount, 'a1_mismatch': a1_bad})
    wjson('partA-reparse.json', {'reparsed_ok_trials': a2_n, 'a2_mismatch': a2_bad})
    wjson('partB-tallies.json', tallies)
    with open(os.path.join(out, 'partC-sheet.jsonl'), 'x', encoding='utf-8', newline=NL) as f:
        for s in sheet:
            f.write(json.dumps(s, ensure_ascii=False) + NL)
    wjson('partC-key.json', key)
    strata = collections.Counter(k['stratum'] for k in key)
    pc = collections.Counter(k['parser_category'] for k in key)
    summ = {'inputs': {'judge_json': jsha, 'parser_lf': psha, 'scenarios_lf': ssha, 'zips': {sc: c['zips'][sc][1] for sc in c['zips']}},
            'a1_mismatch': len(a1_bad), 'a2_mismatch': len(a2_bad), 'a2_reparsed': a2_n,
            'c_items': len(key), 'c_strata': dict(strata), 'c_parser_category': dict(pc),
            'c_echo_removed_items': sum(1 for k in key if k['echo_removed_chars'] > 0),
            'c_stance_phrase_left_items': sum(1 for k in key if k['stance_phrase_left']),
            'outputs': {n: sha_bytes(open(os.path.join(out, n), 'rb').read()) for n in sorted(os.listdir(out))}}
    wjson('open-summary.json', summ)
    print('A1 mismatch', len(a1_bad), '| A2 mismatch', len(a2_bad), '| A2 reparsed', a2_n)
    print('C items', len(key), dict(strata), dict(pc))
    print('C echo removed items', summ['c_echo_removed_items'], '| stance phrase left items', summ['c_stance_phrase_left_items'])
    if a1_bad or a2_bad:
        print('STOP A の違いがある（出力は書いた）')
        raise SystemExit(2)
    print('OK')


if __name__ == '__main__':
    main()
