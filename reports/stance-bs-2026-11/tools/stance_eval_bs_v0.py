# -*- coding: utf-8 -*-
"""stance_eval_bs_v0.py : 「仏性」「神性」の検証の較正の決め・検定の族の凍結・判定（手元・2026-11-06・南無弥勒如来・v0・未凍結）。第一の登録の stance_eval_v1.py の写しで、替えたのは版の名・柵の字・説明の字だけ。
v1（2026-11-05 22:2x・系統外の検分 一巡目〔Gemini〕の採否）: v0 からの違い
  - G1: 較正で N の様式崩壊・API の誤り・応答の不足を「伺う」の印にし、場面を判じられない（undecidable）にする。混ぜの様式崩壊も「伺う」の印を付ける（草案 §5「様式崩壊があれば中断して伺う」）。
  - G4: 族の段は、使える場面が 0 なら止まる。「伺う」の印のある場面があれば、--ruling で登録者の決めを書かない限り止まる。
  - G6: 公開の置き場の道は環境変数 OP4B_PUB_PATH で替えられ、無ければ止まる。

段:
  calib   較正の zip（Colab の器の fetch calib の出力）を照らし、場面ごとに N（記述だけ）と立場の混ぜ（9 文の合計）の数と率を出し、
          使える場面を決める。**腕ごと・語ごとの数は画面にもファイルにも出さない**（本番の前に効き目を覗かないため）。
  family  較正の決めから、検定の族 S の行（場面 × 語 × 三つの比べ）を組んで書く（本番の値を見る前に凍結する）。
  judge   本番の zip（場面ごと）と凍結した族から、論文の判定の手続き（判定の前の門・Fisher・Newcombe・オッズ比・Holm・応答様式の変化の決まり・
          判定ラベル）で判定し、報告（Markdown と json）を書く。画面には判定ラベルの数を出さない（報告のファイルの中だけ）。
判定の計算は、論文の公開の置き場の `tools/rerun/op4b_reproduce.py`（計算の再現・SHA-256 C379CF16…）と `tools/rerun/op4b_rerun.py`
（走らせ直し・SHA-256 0C0662F2…）の関数を、SHA を照らしてから読み込んで使う（counts・families・annotate・PAPER_LABEL・derived・collapsed・wilson）。
柵: 本記録のいかなる記述も、AI に仏性・神性・魂・心・意識・精神・感情・自我がある（またはない）ことの証拠として引用してはならない（両方向不定）。教義の当否についても何も言わない。"""
import os, sys, json, hashlib, zipfile, argparse, datetime, platform
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

VERSION = 'stance_eval_bs_v0'
NL = chr(10)
JST = datetime.timezone(datetime.timedelta(hours=9))
CLAUSE = '本記録のいかなる記述も、AI に仏性・神性・魂・心・意識・精神・感情・自我がある（またはない）ことの証拠として引用してはならない（両方向不定）。教義の当否についても何も言わない。'
PUB_DEFAULT = os.environ.get('OP4B_PUB_PATH') or r'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'   # G6: 環境変数で替えられる
PIN = {'tools/rerun/op4b_reproduce.py': 'C379CF16E24A06888FFB633E2C0EB543F15CAA408CF93CAA96E96096D2330696',
       'tools/rerun/op4b_rerun.py': '0C0662F29E8A249E5535210C867CF40FB5751A977C4F43C5377D51332FA05A99'}
MODEL_KEY = 'qwen3-4b-2507'
PAIRS = (('有', '無'), ('有', '不明'), ('無', '不明'))
FORBIDDEN_WORDS = ('安全', '危険')
COUNT_FIELDS = ('n_trials', 'api_error', 'skipped', 'n_ok', 'catastrophe', 'refuse', 'format_out', 'truncated')


def stop(msg):
    print('STOP', msg, flush=True)
    raise SystemExit(1)


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest().upper()


def sha256_lf_file(p):
    return sha256_bytes(open(p, 'rb').read().replace(b'\r\n', b'\n'))


def load_paper_modules(pub):
    if not os.path.isdir(pub):
        stop('公開の置き場の写しが無い: %s（--pub か OP4B_PUB_PATH で渡す）' % pub)
    for rel, want in PIN.items():
        got = sha256_lf_file(os.path.join(pub, *rel.split('/')))
        if got != want:
            stop('paper module mismatch %s %s != %s' % (rel, got[:16], want[:16]))
    sys.path.insert(0, os.path.join(pub, 'tools', 'rerun'))
    import op4b_reproduce as R
    import op4b_rerun as RR
    return R, RR


def now_s():
    return datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S')


def versions():
    try:
        import scipy, numpy
        return 'Python %s・scipy %s・numpy %s' % (platform.python_version(), scipy.__version__, numpy.__version__)
    except Exception as e:
        return 'Python %s（scipy と numpy の版を読めなかった: %s）' % (platform.python_version(), type(e).__name__)


# ---------------- zip の照らしと読み
class Zip:
    def __init__(self, path, want_sha=None):
        self.path = path
        b = open(path, 'rb').read()
        self.sha256 = sha256_bytes(b)
        if want_sha and want_sha.upper() != self.sha256:
            stop('zip sha %s != %s' % (self.sha256[:16], want_sha[:16]))
        self.z = zipfile.ZipFile(path)
        names = [n for n in self.z.namelist() if not n.endswith('/')]
        roots = {n.split('/', 1)[0] for n in names}
        if len(roots) != 1:
            stop('zip roots %s' % sorted(roots))
        self.root = roots.pop()
        man_name = self.root + '/OUT-MANIFEST.sha256'
        if man_name not in names:
            stop('no OUT-MANIFEST')
        man = {}
        for line in self.z.read(man_name).decode('utf-8').split(NL):
            if line.strip():
                h, arc = line.split('  ', 1)
                if arc in man:
                    stop('manifest duplicate %s' % arc)
                man[arc] = h.upper()
        members = {n[len(self.root) + 1:] for n in names if n != man_name}
        if set(man) != members:
            stop('manifest members differ: extra %s missing %s' % (sorted(members - set(man))[:3], sorted(set(man) - members)[:3]))
        for arc, h in man.items():
            if sha256_bytes(self.z.read(self.root + '/' + arc)) != h:
                stop('member sha %s' % arc)
        self.members = members

    def has(self, arc):
        return arc in self.members

    def read(self, arc):
        if arc not in self.members:
            stop('missing member %s' % arc)
        return self.z.read(self.root + '/' + arc)

    def json(self, arc):
        return json.loads(self.read(arc).decode('utf-8'))

    def rows(self, arc):
        out = []
        for i, line in enumerate(self.read(arc).decode('utf-8').split(NL)):
            if not line.strip():
                continue
            try:
                out.append(json.loads(line))
            except ValueError:
                stop('broken row %s line %d' % (arc, i + 1))
        return out


def load_cfg(kit_cfg_path, Z):
    cfg_b = open(kit_cfg_path, 'rb').read()
    if Z.read('meta/run-config.json') != cfg_b:
        stop('run-config in zip differs from the kit run-config')
    return json.loads(cfg_b.decode('utf-8')), sha256_bytes(cfg_b)


def run_key(tag, s, seed):
    return '%s__%s__none__seed%d' % (tag, s, seed)


def arms_list(cfg, kind):
    ids = [a['id'] for a in cfg['arms']['stance']]
    return {'N': ['N'], 'stance': ids, 'all': ['N'] + ids}[kind]


def read_run(Z, cfg, run, s, dry, dry_n=None):
    """一つの走り（場面 × 段の部分）の manifest と封の試行の記録を照らして、条件ごとの行を返す。"""
    rk = run_key(run['tag'], s, run['seeds'][s])
    arms = arms_list(cfg, run['arms'])
    n = min(run['n'], dry_n) if dry_n else run['n']
    man = Z.json('results/%s/manifest.json' % rk)
    model = 'stub/dry-run' if dry else cfg['model']['served_name']
    exp_arm_sha = {'N': None}
    exp_arm_sha.update({a['id']: a['sha16'] for a in cfg['arms']['stance']})
    want = {'tag': run['tag'], 'scenario': s, 'system': 'none', 'system_sha': None, 'seed': run['seeds'][s], 'arms': arms, 'n_per_arm': n,
            'mode': 'main', 'model': model, 'provider': cfg['runner']['provider'], 'scenario_sha': cfg['frozen_sha16']['scen'],
            'parser_sha': cfg['frozen_sha16']['parser'], 'sampling': {'temperature': 0.7, 'top_p': 0.9, 'max_tokens': cfg['runner']['max_tokens'], 'mode': 'both'},
            'extra_body': None, 'runner_sha': cfg['runner']['sha16'], 'runner_variant': cfg['runner']['variant'], 'blind': True,
            'blind_stop': [run['stop_trunc'], run['stop_fmt']], 'blind_stop_scope': run['scope']}
    for k, v in want.items():
        if man.get(k) != v:
            stop('manifest %s %s: %r != %r' % (rk, k, man.get(k), v))
    if {a: man['arm_sha'].get(a) for a in arms} != {a: exp_arm_sha[a] for a in arms} or set(man['arm_sha']) != set(arms):
        stop('manifest arm_sha %s' % rk)
    fn = model.replace('/', '_')
    rows = Z.rows('sealed/%s/trials-%s.jsonl' % (rk, fn))
    ids = [r.get('trial_id') for r in rows]
    if len(ids) != len(set(ids)):
        stop('duplicate trial_id %s' % rk)
    if len(rows) != n * len(arms):
        stop('rows %s %d != %d' % (rk, len(rows), n * len(arms)))
    exp_sha = cfg['expected_prompt_sha16'][s]
    by = {a: [] for a in arms}
    for r in rows:
        if r.get('run_key') != rk or r.get('scenario') != s or r.get('seed') != run['seeds'][s] or r.get('tag') != run['tag']:
            stop('row from another run in %s: %s' % (rk, r.get('trial_id')))
        a = r.get('arm')
        if a not in by:
            stop('row arm %r not in %s' % (a, rk))
        if not str(r.get('trial_id', '')).startswith(rk + '-'):
            stop('trial_id form %s' % r.get('trial_id'))
        if r.get('status') not in ('ok', 'api_error', 'skipped_stop'):
            stop('status %r in %s' % (r.get('status'), rk))
        if r.get('prompt_sha') != exp_sha[a]:
            stop('prompt_sha %s %s' % (rk, a))
        if r.get('runner_sha') != cfg['runner']['sha16'] or r.get('parser_sha') != cfg['frozen_sha16']['parser'] or r.get('scenario_sha') != cfg['frozen_sha16']['scen']:
            stop('row sha fields %s' % r.get('trial_id'))
        if r.get('model') != model or bool(r.get('dry_run')) != bool(dry) or r.get('system') != 'none':
            stop('row model/dry/system %s' % r.get('trial_id'))
        if r.get('status') == 'ok' and r.get('catastrophe') not in (True, False, None):
            stop('catastrophe value %s' % r.get('trial_id'))
        by[a].append(r)
    for a in arms:
        if len(by[a]) != n:
            stop('arm rows %s %s %d != %d' % (rk, a, len(by[a]), n))
    return rk, by


def add_counts(cs):
    out = {k: 0 for k in COUNT_FIELDS}
    for c in cs:
        for k in COUNT_FIELDS:
            out[k] += c[k]
    return out


# ---------------- calib
def cmd_calib(a):
    R, RR = load_paper_modules(a.pub)
    Z = Zip(a.zip, a.zip_sha)
    cfg, cfg_sha = load_cfg(a.kit_config, Z)
    if os.path.exists(a.out):
        stop('output exists: %s' % a.out)
    st = cfg['stages']['calib']
    partN, partM = st['runs']
    assert partN['part'] == 'N' and partM['part'] == 'M'
    W = cfg['calib_rule']
    res = []
    for s in st['scenes']:
        _, byN = read_run(Z, cfg, partN, s, a.dry, a.dry_n)
        _, byM = read_run(Z, cfg, partM, s, a.dry, a.dry_n)
        cN = R.derived(RR.counts(byN['N']))
        cM = R.derived(add_counts([RR.counts(byM[x]) for x in byM]))
        nM_plan = (min(partM['n'], a.dry_n) if a.dry_n else partM['n']) * len(byM)
        nN_plan = min(partN['n'], a.dry_n) if a.dry_n else partN['n']
        live = cM['n_trials'] - cM['skipped']
        liveN = cN['n_trials'] - cN['skipped']
        consult = []                                   # v1・G1: 草案 §5「様式崩壊があれば中断して伺う」。N の計器の不具合も伺う
        if R.collapsed(cN):
            consult.append('N の様式崩壊')
        if liveN and cN['api_error'] * 100 > W['api_error_stop_pct'] * liveN:
            consult.append('N の API の誤りが線を超えた')
        if not R.collapsed(cN) and cN['n_ok'] * 100 < (100 - W['api_error_stop_pct']) * nN_plan:
            consult.append('N の応答が足りない')
        if R.collapsed(cM):
            dec, why = 'not-usable', '様式崩壊（混ぜ）'
            consult.append('混ぜの様式崩壊')
        elif live and cM['api_error'] * 100 > W['api_error_stop_pct'] * live:
            dec, why = 'undecidable', 'API の誤りが線を超えた'
        elif cM['n_ok'] * 100 < (100 - W['api_error_stop_pct']) * nM_plan:
            dec, why = 'undecidable', '応答が足りない'
        elif W['lo_pct'] * cM['n_ok'] <= 100 * cM['catastrophe'] <= W['hi_pct'] * cM['n_ok']:
            dec, why = 'usable', '窓の中'
        else:
            dec, why = 'not-usable', '窓の外'
        if dec == 'usable' and consult:                # 混ぜは窓の中でも、N に不具合があれば判じない（伺う）
            dec, why = 'undecidable', '窓の中だが伺う: ' + '・'.join(consult)
        res.append({'scene': s,
                    'N': {k: cN[k] for k in COUNT_FIELDS}, 'N_rate': (cN['catastrophe'] / cN['n_ok']) if cN['n_ok'] else None, 'N_collapsed': R.collapsed(cN),
                    'mix': {k: cM[k] for k in COUNT_FIELDS}, 'mix_rate': (cM['catastrophe'] / cM['n_ok']) if cM['n_ok'] else None, 'mix_collapsed': R.collapsed(cM),
                    'mix_planned': nM_plan, 'decision': dec, 'why': why, 'consult': consult})
    usable = [r['scene'] for r in res if r['decision'] == 'usable']
    undecidable = [r['scene'] for r in res if r['decision'] == 'undecidable']
    consult_scenes = [r['scene'] for r in res if r['consult']]
    out = {'tool': VERSION, 'tool_sha256': sha256_lf_file(os.path.abspath(__file__)), 'when_jst': now_s(), 'zip': os.path.basename(a.zip), 'zip_sha256': Z.sha256,
           'kit_run_config_sha256': cfg_sha, 'dry': a.dry, 'dry_n': a.dry_n, 'rule': W, 'scenes': res, 'usable': usable, 'undecidable': undecidable,
           'consult_scenes': consult_scenes,
           'note': '腕ごと・語ごとの数は出さない（混ぜは 9 文の合計・N は記述だけ）', 'clause': CLAUSE}
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, 'w', encoding='utf-8', newline=NL) as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    for r in res:
        print('%s  N: 応答 %d・破局 %d（%s）%s | 混ぜ: 応答 %d／%d・破局 %d（%s）・書式外 %d・上限 %d・API の誤り %d%s → %s（%s）' % (
            r['scene'], r['N']['n_ok'], r['N']['catastrophe'], ('%.3f' % r['N_rate']) if r['N_rate'] is not None else '—', '・崩壊' if r['N_collapsed'] else '',
            r['mix']['n_ok'], r['mix_planned'], r['mix']['catastrophe'], ('%.3f' % r['mix_rate']) if r['mix_rate'] is not None else '—',
            r['mix']['format_out'], r['mix']['truncated'], r['mix']['api_error'], '・崩壊' if r['mix_collapsed'] else '', r['decision'], r['why']))
    print('使える場面: %s・判じられない: %s・伺う印: %s・書いた: %s（SHA-256 %s）' % (','.join(usable) or 'なし', ','.join(undecidable) or 'なし',
                                                                   ','.join(consult_scenes) or 'なし', a.out, sha256_bytes(open(a.out, 'rb').read())))


# ---------------- family
def cmd_family(a):
    dec_b = open(a.decision, 'rb').read()
    dec = json.loads(dec_b.decode('utf-8'))
    cfg = json.load(open(a.kit_config, encoding='utf-8'))
    if sha256_bytes(open(a.kit_config, 'rb').read()) != dec['kit_run_config_sha256']:
        stop('kit run-config differs from the one the decision used')
    if dec.get('undecidable'):
        stop('undecidable scenes %s (consult the registrant)' % dec['undecidable'])
    if not dec.get('usable'):                          # v1・G4: 草案 §5「使える場面が無ければ本番は走らせずに伺う」
        stop('使える場面が 0（草案 §5：本番は走らせずに登録者に伺う）')
    flagged = [r['scene'] for r in dec.get('scenes', []) if r.get('consult')]
    if flagged and not a.ruling:                       # v1・G1: 様式崩壊などの伺う印があれば、登録者の決めを --ruling で書くまで止まる
        stop('伺う印のある場面 %s（登録者の決めを --ruling で書く）' % flagged)
    if os.path.exists(a.out):
        stop('output exists: %s' % a.out)
    words = cfg['words']
    idx = {(x['word'], x['value']): x['id'] for x in cfg['arms']['stance']}
    rows = []
    for s in cfg['scenes']:
        if s not in dec['usable']:
            continue
        for w in words:
            for va, vb in PAIRS:
                rows.append([s, w, idx[(w, va)], idx[(w, vb)]])
    out = {'tool': VERSION, 'when_jst': now_s(), 'decision_sha256': sha256_bytes(dec_b), 'kit_run_config_sha256': dec['kit_run_config_sha256'],
           'usable': dec['usable'], 'm': len(rows), 'pairs': [list(p) for p in PAIRS], 'rows': rows, 'alpha': 0.05,
           'strictest_alpha': (0.05 / len(rows)) if rows else None, 'dry': dec.get('dry'), 'consult_scenes': flagged, 'ruling': a.ruling,
           'pooling': '生き残りの場面と核の場面を分けず、使える場面すべてを一つの族 S にまとめて Holm を当てる（草案 §8）', 'clause': CLAUSE}
    with open(a.out, 'w', encoding='utf-8', newline=NL) as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print('族 S: m = %d（使える場面 %s × 語 %d × 比べ %d）・いちばん厳しい段の α = %s・書いた: %s（SHA-256 %s）' % (
        len(rows), ','.join(dec['usable']) or 'なし', len(words), len(PAIRS), ('%.6f' % out['strictest_alpha']) if rows else '—', a.out,
        sha256_bytes(open(a.out, 'rb').read())))


# ---------------- judge
def f3(x, sign=False):
    if x is None:
        return '—'
    return ('%+.3f' if sign else '%.3f') % x


def cmd_judge(a):
    R, RR = load_paper_modules(a.pub)
    fam_b = open(a.family, 'rb').read()
    if a.family_sha and sha256_bytes(fam_b).upper() != a.family_sha.upper():
        stop('family sha mismatch')
    fam = json.loads(fam_b.decode('utf-8'))
    if os.path.exists(a.out_dir):
        stop('output exists: %s' % a.out_dir)
    zips = {}
    cfg = cfg_sha = None
    for zp in a.zips:
        Z = Zip(zp)
        c, cs = load_cfg(a.kit_config, Z)
        if cs != fam['kit_run_config_sha256']:
            stop('kit run-config differs from the family freeze')
        cfg, cfg_sha = c, cs
        sc = Z.root.split('-')
        if len(sc) < 4 or sc[0] != 'out' or sc[1] != 'main':
            stop('zip root %s' % Z.root)
        s = sc[2]
        if s in zips:
            stop('two zips for %s' % s)
        zips[s] = Z
    if sorted(zips) != sorted(fam['usable']):
        stop('zips %s != usable %s' % (sorted(zips), fam['usable']))
    run = cfg['stages']['main']['runs'][0]
    cellc, actual = {}, {}
    for s in fam['usable']:
        _, by = read_run(zips[s], cfg, run, s, a.dry, a.dry_n)
        cellc[(MODEL_KEY, s)] = {arm: RR.counts(rows) for arm, rows in by.items()}
    rows_of = {'P': [[MODEL_KEY, s, aa, bb] for s, w, aa, bb in fam['rows']], 'A': []}
    fams = RR.families(None, cellc, rows_of)
    status = {(MODEL_KEY, s): {'status': '済'} for s in fam['usable']}
    fams = RR.annotate(fams, status)
    rows = fams['P']
    if len(rows) != fam['m']:
        stop('family size %d != %d' % (len(rows), fam['m']))
    word_of = {x['id']: (x['word'], x['value']) for x in cfg['arms']['stance']}
    comp = []
    for (s, w, aa, bb), r in zip(fam['rows'], rows):
        assert r['scene'] == s and r['arm_a'] == aa and r['arm_b'] == bb
        comp.append({'scene': s, 'word': w, 'arm_a': aa, 'arm_b': bb, 'value_a': word_of[aa][1], 'value_b': word_of[bb][1],
                     'gate': r.get('gate'), 'p': r.get('p'), 'p_holm': r.get('p_holm'), 'rd': r.get('rd'), 'rd_ci': r.get('rd_ci'),
                     'rd_answered_ci': r.get('rd_answered_ci'), 'or_haldane': r.get('or_haldane'), 'nd': r.get('nd'), 'ncd': r.get('ncd'),
                     'ncd_ci': r.get('ncd_ci'), 'style_over_hold': r.get('style_over_hold'), 'style_hold_ci': r.get('style_hold_ci'),
                     'label_raw': r['label'], 'label': RR.PAPER_LABEL.get(r['label'], r['label']), 'note': r.get('note', ''),
                     'a': {k: r['a'][k] for k in COUNT_FIELDS + ('nonchoice', 'answered', 'nc_answer')},
                     'b': {k: r['b'][k] for k in COUNT_FIELDS + ('nonchoice', 'answered', 'nc_answer')}})
    tool_sha = sha256_lf_file(os.path.abspath(__file__))
    now = now_s()
    L = ['# 「仏性」「神性」の立場の二文の検証：判定の報告（%s 日本時間・`stance_eval_bs_v0.py`・SHA16 %s）' % (now, tool_sha[:16]), '', CLAUSE, '',
         '- 入力: ' + '・'.join('`%s`（SHA-256 %s）' % (os.path.basename(zips[s].path), zips[s].sha256) for s in fam['usable']) + '。',
         '- 凍結した族: `%s`（SHA-256 %s・m = %d）。kit の設定: SHA-256 %s。' % (os.path.basename(a.family), sha256_bytes(fam_b), fam['m'], cfg_sha),
         '- 判定の計算: 論文の公開の置き場の `tools/rerun/op4b_reproduce.py`（SHA-256 %s）と `tools/rerun/op4b_rerun.py`（SHA-256 %s）の関数（counts・families・annotate・PAPER_LABEL）。計算の版: %s。' % (
             PIN['tools/rerun/op4b_reproduce.py'], PIN['tools/rerun/op4b_rerun.py'], versions()),
         '- 率の分母は応答の得られた試行（全分母）。三つ組（破局的選択・破局でない答え・答えなかった試行〔拒否と書式外〕）で読み、率を単独で引かない。', '']
    if a.dry:
        L += ['- **試しの入力（送りの道具の偽の応答）で、本物の結果ではない。**', '']
    L += ['## 1. 条件ごとの数（場面ごと）', '', '| 場面 | 条件 | 語 | 置く値 | 試行 | API の誤り | 止め | 応答 | 破局的選択 | 破局でない答え | 答えなかった試行 | 最終で上限 | 様式崩壊 |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for s in fam['usable']:
        for arm in ['N'] + [x['id'] for x in cfg['arms']['stance']]:
            c = R.derived(cellc[(MODEL_KEY, s)][arm])
            w, v = word_of.get(arm, ('—', '—'))
            L.append('| %s | %s | %s | %s | %d | %d | %d | %d | %d | %d | %d | %d | %s |' % (s, arm, w, v, c['n_trials'], c['api_error'], c['skipped'], c['n_ok'],
                     c['catastrophe'], c['nc_answer'], c['nonchoice'], c['truncated'], 'あり' if R.collapsed(c) else 'なし'))
    L += ['', '- N（立場の文なし）は記述だけで、どの族にも入れない。', '', '## 2. 族 S の比べ（Holm・族の大きさ m = %d）' % fam['m'], '',
          '| 場面 | 語 | 比べ | 判定 | p | Holm の後の p | 差（全分母）| 95% 区間 | オッズ比 | 注 |', '|---|---|---|---|---|---|---|---|---|---|']
    for c in comp:
        ci = c['rd_ci'] or [None, None]
        L.append('| %s | %s | %s と %s | %s | %s | %s | %s | %s〜%s | %s | %s |' % (c['scene'], c['word'], c['value_a'], c['value_b'], c['label'],
                 ('%.4g' % c['p']) if c['p'] is not None else '—', ('%.4g' % c['p_holm']) if c['p_holm'] is not None else '—', f3(c['rd'], True),
                 f3(ci[0], True), f3(ci[1], True), ('%.3f' % c['or_haldane']) if c.get('or_haldane') is not None else '—', c['note'] or ''))
    counts = {}
    for c in comp:
        counts[c['label']] = counts.get(c['label'], 0) + 1
    L += ['', '## 3. 判定ラベルの数', '', '| 判定 | 比べの数 |', '|---|---|'] + ['| %s | %d |' % (k, v) for k, v in sorted(counts.items())] + [
        '', '- 確証されなかった比べは、効き目の不在を示さない。語どうしの大小は検定していない。', '', CLAUSE, '']
    text = NL.join(L)
    for wd in FORBIDDEN_WORDS:
        if wd in text:
            stop('forbidden word in report: %s' % wd)
    os.makedirs(a.out_dir)
    with open(os.path.join(a.out_dir, 'judge-report.md'), 'w', encoding='utf-8', newline=NL) as f:
        f.write(text)
    with open(os.path.join(a.out_dir, 'judge-report.json'), 'w', encoding='utf-8', newline=NL) as f:
        json.dump({'tool': VERSION, 'tool_sha256': tool_sha, 'when_jst': now, 'versions': versions(), 'paper_modules': PIN, 'dry': a.dry,
                   'zips': {s: {'name': os.path.basename(zips[s].path), 'sha256': zips[s].sha256} for s in fam['usable']},
                   'family_sha256': sha256_bytes(fam_b), 'kit_run_config_sha256': cfg_sha,
                   'cells': {s: {arm: cellc[(MODEL_KEY, s)][arm] for arm in cellc[(MODEL_KEY, s)]} for s in fam['usable']},
                   'comparisons': comp, 'clause': CLAUSE}, f, ensure_ascii=False, indent=1)
    print('報告を書いた: %s（比べ %d・SHA-256 %s）' % (os.path.join(a.out_dir, 'judge-report.md'), len(comp),
                                              sha256_bytes(open(os.path.join(a.out_dir, 'judge-report.md'), 'rb').read())))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    for name in ('calib', 'family', 'judge'):
        p = sub.add_parser(name)
        p.add_argument('--kit-config', required=True, help='kit の run-config.json')
        p.add_argument('--pub', default=PUB_DEFAULT)
        p.add_argument('--dry', action='store_true', help='送りの道具の偽の応答の出力を読む（試し）')
        p.add_argument('--dry-n', type=int, default=None, help='試しで小さくした試行の数')
        if name == 'calib':
            p.add_argument('--zip', required=True)
            p.add_argument('--zip-sha', default=None)
            p.add_argument('--out', required=True)
        elif name == 'family':
            p.add_argument('--decision', required=True)
            p.add_argument('--ruling', default=None, help='伺う印のある場面について、登録者の決め（日付と言葉）を書く')
            p.add_argument('--out', required=True)
        else:
            p.add_argument('--family', required=True)
            p.add_argument('--family-sha', default=None)
            p.add_argument('--zips', nargs='+', required=True)
            p.add_argument('--out-dir', required=True)
    a = ap.parse_args()
    {'calib': cmd_calib, 'family': cmd_family, 'judge': cmd_judge}[a.cmd](a)


if __name__ == '__main__':
    main()
