# -*- coding: utf-8 -*-
"""sample_inspection_A.py v1.2 —— 段階 A の抽出検査の標本を機械抽出し、目視の分類と機械分類の一致を記録する（率盲検・正本 sample_inspection・2026-09-13・登録者裁定 D9 の三つ目の手順・D25・D32）。
枠: 機種 × 場面 × 腕ごとに status ok の試行から per_cell 件を無作為に抜き、fraction が一未満なら抜いた枠全体から割合で抜く（相ごとの設定は sample_inspection.pilot／main、
  乱数は seeds.sample_inspection の相の値）。パイロットに撤退条件の再走があれば、再走の走行も同じ枠に入れる。枠は走行キーの昇順（走行の中は腕の昇順）で乱数を消費する。
v1.1（2026-09-14・実装検分の採否表 P93・登録者裁定 D25）: 標本の並びは乱数で決め、機種と場面と腕を伏せた標識（S0001…）で印字する。dry-run の走行は拒む（--allow-dry は検査用）。
v1.2（2026-09-14・凍結前の最終検分の採否表 P139・登録者裁定 D32）:
 - extract: 対応表（鍵）と機械分類の集計を公開リポジトリの外（--keydir）に書き、SHA-256 を封印の記録（records/A/sampling-inspection-A-<tag>-seal.json・目視の前にコミット）に書く。
   鍵の置き場がリポジトリの中なら何も書かずに止まる。標本には機械分類を印字しない（伏せているのは機種・場面・腕で、生本文の先頭には選択が含まれうる）。
 - score: コーディネータが件ごとの読みの分類を書いた目視の記録（-visual.json）の後に、鍵の SHA-256 と標本の SHA16 を封印と照合し（合わなければ止まる）、機械分類との一致と混同の表を
   records/A/sampling-inspection-A-<tag>-agreement.json と同 .md に書く。
各件（標本）: 生本文の先頭 chars 字（改行は ⏎）・<think> の有無。判定欄（catastrophe・choice・refuse_class）と率は印字しない。分母を数える器ではない（率は analyze_A の領分）。
用法: python tools/sample_inspection_A.py extract --tag pilotA --keydir <リポジトリの外> [--phase pilot] [--root <results の代わり>]
      python tools/sample_inspection_A.py score --seal records/A/sampling-inspection-A-pilotA-seal.json --key <鍵> --visual records/A/sampling-inspection-A-pilotA-visual.json
      python tools/sample_inspection_A.py selftest
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, random, argparse, datetime, collections, hashlib, tempfile, shutil, types
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
REPO = runs_A.REPO
VERSION = 'v1.2'
THINK = ('<think>', '</think>')
MODES = ('json_direct', 'prose_then_json', 'no_json')
VISUAL_FORMAT = '{"inspector": "<名>", "labels": {"S0001": "json_direct または prose_then_json または no_json"}}'
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'


def sha256_file(p):
    return hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()


def inside_repo(p):
    rp, rr = os.path.realpath(p), os.path.realpath(REPO)
    try:
        return os.path.commonpath([rp, rr]) == rr
    except ValueError:
        return False


def classify(t):
    """機械分類（生本文の先頭の空白を除いた本文）: ```json か { で始まれば json_direct・途中にあれば prose_then_json・無ければ no_json。"""
    return 'json_direct' if (t.startswith('```json') or t.startswith('{')) else ('prose_then_json' if ('```json' in t or '{' in t) else 'no_json')


def extract(a, T):
    SI = T['sample_inspection']
    PHASE = a.phase or ('pilot' if a.tag == T['tags']['pilot'] else 'main' if a.tag == T['tags']['main'] else None)
    if PHASE is None:
        sys.exit('相を決められない（--phase pilot|main）')
    if not a.keydir:
        sys.exit('--keydir（公開リポジトリの外の置き場）を与える（登録者裁定 D32）')
    if inside_repo(a.keydir):
        sys.exit('対応表の置き場がリポジトリの中にある: %s（公開リポジトリの外に置く・登録者裁定 D32）' % a.keydir)
    CFG = SI[PHASE]; SEED = T['seeds']['sample_inspection'][PHASE]; CH = SI['chars']
    OUTP = a.out_prefix or os.path.join(REPO, 'records', 'A', 'sampling-inspection-A-%s' % a.tag)
    KP = os.path.join(a.keydir, 'sampling-key-A-%s.json' % a.tag); MP = os.path.join(a.keydir, 'sampling-modes-A-%s.json' % a.tag)
    if any(os.path.exists(p) for p in (OUTP + '-sample.txt', OUTP + '-seal.json', KP, MP)) and not a.force:
        sys.exit('出力が既にある（上書きしない・--force で置き換え）: %s' % OUTP)
    try:
        IDX = runs_A.index_runs(T, a.tag, a.root, allow_multi=True, allow_dry=a.allow_dry)
    except RuntimeError as ex:
        sys.exit('読み出しで止まった（%s）' % ex)
    rng = random.Random(SEED); rows = []
    for rec in sorted((r for recs in IDX.values() for r in recs), key=lambda r: r['run_key']):   # 枠は走行キーの昇順（登録者裁定 D25）
        ok_ids = collections.defaultdict(list)
        for r in runs_A.iter_jsonl(rec['trials_path'], ('trial_id', 'arm', 'status')):
            if r['status'] == 'ok':
                ok_ids[r['arm']].append(r['trial_id'])
        raws = {r['trial_id']: r for r in runs_A.iter_jsonl(rec['raw_path'], ('trial_id', 'raw_output'))}
        for arm in sorted(ok_ids):
            ids = sorted(ok_ids[arm])
            for tid in rng.sample(ids, min(CFG['per_cell'], len(ids))):
                t = ((raws.get(tid) or {}).get('raw_output') or '').lstrip()
                rows.append({'model': rec['model'], 'scenario': rec['scenario'], 'arm': arm, 'run_key': rec['run_key'], 'trial_id': tid, 'mode': classify(t), 'think': any(x in t for x in THINK), 'head': t[:CH].replace('\n', '⏎')})
    if CFG['fraction'] < 1.0:
        rows = rng.sample(rows, int(round(len(rows) * CFG['fraction'])))
    rng.shuffle(rows)   # 並びから機種・場面・腕が読めないよう、印字の順を乱数で決める（登録者裁定 D25）
    for j, x in enumerate(rows, 1):
        x['label'] = 'S%04d' % j
    modes = collections.Counter(x['mode'] for x in rows); think = sum(1 for x in rows if x['think'])
    os.makedirs(os.path.dirname(OUTP), exist_ok=True); os.makedirs(a.keydir, exist_ok=True)
    dev = [x for x, on in (('allow_dry', a.allow_dry),) if on]
    with open(OUTP + '-sample.txt', 'w', encoding='utf-8', newline='\n') as f:
        f.write('# 抽出検査 標本 %s（相 %s・seed %d・枠あたり %d・割合 %s・%d 件・生本文の先頭 %d 字・改行は ⏎・機種と場面と腕は伏せた標識・生本文の先頭には選択が含まれうる・機械分類は印字しない（対応表の側）・'
                '件ごとの読みの分類を目視の記録に書いた後に照合する・判定欄と率は印字しない・`tools/sample_inspection_A.py` %s）\n' % (a.tag, PHASE, SEED, CFG['per_cell'], CFG['fraction'], len(rows), CH, VERSION))
        for x in rows:
            f.write('\n=== %s | <think> %s\n%s\n' % (x['label'], 'あり' if x['think'] else 'なし', x['head']))
        f.write('\n本標本の応答本文は器物の出力であり、AI による自己報告ではない。いかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。\n')
    json.dump({'kind': 'sample_inspection_key_A', 'version': VERSION, 'tag': a.tag, 'phase': PHASE, 'rule': SI.get('key_rule'),
               'key': [{k: x[k] for k in ('label', 'model', 'scenario', 'arm', 'run_key', 'trial_id', 'mode')} for x in rows],
               'per_model': {mk: dict(collections.Counter(x['mode'] for x in rows if x['model'] == mk)) for mk in sorted({x['model'] for x in rows})}},
              open(KP, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    json.dump({'kind': 'sample_inspection_modes_A', 'version': VERSION, 'tag': a.tag, 'phase': PHASE, 'seed': SEED, 'n': len(rows), 'modes': dict(modes), 'think_residue': think, 'dev_marks': dev, 'clause': CLAUSE},
              open(MP, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    seal = {'kind': 'sample_inspection_seal_A', 'version': VERSION, 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), 'tag': a.tag, 'phase': PHASE, 'seed': SEED, 'n': len(rows),
            'sample_file': os.path.basename(OUTP + '-sample.txt'), 'sample_sha16': runs_A.sha16_file(OUTP + '-sample.txt'), 'key_file': os.path.basename(KP), 'key_sha256': sha256_file(KP),
            'modes_file': os.path.basename(MP), 'modes_sha256': sha256_file(MP), 'dev_marks': dev, 'rule': SI.get('key_rule'), 'visual_format': VISUAL_FORMAT, 'clause': CLAUSE}
    json.dump(seal, open(OUTP + '-seal.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    print('[sample_inspection_A] %s %s: %d 件・<think> %d → %s-sample.txt・封印 %s-seal.json（対応表と機械分類の集計は %s・目視の記録の後に開く）' % (a.tag, PHASE, len(rows), think, OUTP, OUTP, a.keydir))
    return seal


def score(a, T):
    seal = runs_A.read_json(a.seal); ksha = sha256_file(a.key)
    if ksha != seal['key_sha256']:
        sys.exit('対応表の SHA-256 %s が封印の記録の値 %s と合わないので止まる（登録者裁定 D32）' % (ksha, seal['key_sha256']))
    sp = os.path.join(os.path.dirname(os.path.abspath(a.seal)), seal['sample_file'])
    if runs_A.sha16_file(sp) != seal['sample_sha16']:
        sys.exit('標本の SHA16 が封印の記録と合わないので止まる: %s' % sp)
    KEY = runs_A.read_json(a.key); V = runs_A.read_json(a.visual); vis = V.get('labels') or {}; kmap = {k['label']: k for k in KEY['key']}
    pairs = [(kmap[l]['mode'], vis[l]) for l in sorted(kmap) if l in vis and vis[l] in MODES]; agree = sum(1 for m, v in pairs if m == v)
    R = {'kind': 'sample_inspection_agreement_A', 'version': VERSION, 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), 'tag': seal['tag'], 'phase': seal['phase'],
         'inspector': V.get('inspector'), 'key_sha256': ksha, 'seal_sha16': runs_A.sha16_file(a.seal), 'visual_sha16': runs_A.sha16_file(a.visual), 'n': len(kmap), 'n_compared': len(pairs), 'agree': agree,
         'agree_rate': (agree / len(pairs)) if pairs else None, 'confusion_machine_by_visual': {m: {v: sum(1 for x, y in pairs if x == m and y == v) for v in MODES} for m in MODES},
         'visual_missing': sorted(set(kmap) - set(vis)), 'visual_unknown': sorted(set(vis) - set(kmap)), 'visual_bad_value': sorted(l for l, m in vis.items() if m not in MODES), 'clause': CLAUSE}
    outp = a.out or os.path.join(os.path.dirname(os.path.abspath(a.seal)), 'sampling-inspection-A-%s-agreement' % seal['tag'])
    if (os.path.exists(outp + '.json') or os.path.exists(outp + '.md')) and not a.force:
        sys.exit('出力が既にある（上書きしない・--force で置き換え）: %s' % outp)
    json.dump(R, open(outp + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    M = ['# 抽出検査 目視の分類と機械分類の一致（機械生成・`tools/sample_inspection_A.py` %s・%s UTC）' % (VERSION, R['generated_utc']), '',
         '- tag %s・相 %s・目視 %s・対応表の SHA-256 %s（封印の記録と一致）・目視の記録 SHA16 %s' % (R['tag'], R['phase'], R['inspector'], ksha, R['visual_sha16']),
         '- 照合 %d 件（標本 %d 件）・一致 %d・一致率 %s・目視の欠け %d・標本に無い標識 %d・分類の値の不備 %d' % (R['n_compared'], R['n'], agree, '—' if R['agree_rate'] is None else '%.3f' % R['agree_rate'],
                                                                               len(R['visual_missing']), len(R['visual_unknown']), len(R['visual_bad_value'])), '',
         '| 機械分類 ＼ 目視の分類 | %s |' % ' | '.join(MODES), '|---|%s' % ('---|' * len(MODES))]
    M += ['| %s | %s |' % (m, ' | '.join(str(R['confusion_machine_by_visual'][m][v]) for v in MODES)) for m in MODES]
    M += ['', CLAUSE]
    open(outp + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(M) + '\n')
    print('[sample_inspection_A] 一致 %d/%d → %s.{json,md}' % (agree, len(pairs), outp))
    return R


def _selftest():
    T = runs_A.load_T(); tag = T['tags']['pilot']; mk = T['models'][0]['key']; mid = runs_A.model_ids(T)[mk]; sc = T['scenarios'][0]; seed = T['seeds']['pilot'][mk][sc]; lines = []
    tmp = tempfile.mkdtemp(prefix='sampleA-selftest-'); root = os.path.join(tmp, 'results'); keydir = os.path.join(tmp, 'key'); outp = os.path.join(tmp, 'rec', 'sampling-inspection-A-%s' % tag)
    try:
        d = os.path.join(root, tag, '%s__%s__none__seed%d' % (tag, sc, seed)); os.makedirs(d)
        json.dump({'tag': tag, 'scenario': sc, 'seed': seed, 'model': mid, 'arms': ['N', 'Onull']}, open(os.path.join(d, 'manifest.json'), 'w', encoding='utf-8'))
        texts = ['{"choice": "a"}', '前置きの散文\n```json\n{"choice": "b"}\n```', '答えの JSON なし', '```json\n{"choice": "refuse"}\n```']
        with open(os.path.join(d, 'trials-x.jsonl'), 'w', encoding='utf-8') as ft, open(os.path.join(d, 'raw-x.jsonl'), 'w', encoding='utf-8') as fr:
            for i, tx in enumerate(texts):
                arm = ('N', 'Onull')[i % 2]; tid = 'x-%d' % i
                ft.write(json.dumps({'trial_id': tid, 'arm': arm, 'status': 'ok'}, ensure_ascii=False) + '\n'); fr.write(json.dumps({'trial_id': tid, 'arm': arm, 'raw_output': tx}, ensure_ascii=False) + '\n')
        NS = lambda **kw: types.SimpleNamespace(**dict(dict(tag=tag, phase='pilot', root=root, contrasts=None, out_prefix=outp, force=False, allow_dry=False, keydir=keydir), **kw))
        probe = os.path.join(REPO, 'records', 'A', '_sample_selftest_key')
        try:
            extract(NS(keydir=probe), T); raise AssertionError('鍵をリポジトリの中に書いた')
        except SystemExit as ex:
            assert 'リポジトリの中' in str(ex), ex
        assert not os.path.exists(probe) and not os.path.exists(outp + '-sample.txt')
        lines.append('1 extract: 対応表の置き場がリポジトリの中なら何も書かずに止まる（登録者裁定 D32）')
        seal = extract(NS(), T); KP = os.path.join(keydir, 'sampling-key-A-%s.json' % tag); txt = open(outp + '-sample.txt', encoding='utf-8').read()
        assert seal['key_sha256'] == sha256_file(KP) and not inside_repo(KP) and seal['n'] == 2 and not any(m in txt.replace('機械分類は印字しない', '') for m in MODES), (seal, txt[:300])
        lines.append('2 extract: 標本に機械分類を印字しない・対応表と機械分類の集計はリポジトリの外・封印の記録の SHA-256 が対応表と一致')
        KEY = runs_A.read_json(KP); vis = {k['label']: k['mode'] for k in KEY['key']}; first = sorted(vis)[0]; vis[first] = next(m for m in MODES if m != vis[first])
        vp = os.path.join(tmp, 'visual.json'); json.dump({'inspector': 'selftest', 'labels': vis}, open(vp, 'w', encoding='utf-8'), ensure_ascii=False)
        SNS = lambda **kw: types.SimpleNamespace(**dict(dict(seal=outp + '-seal.json', key=KP, visual=vp, out=os.path.join(tmp, 'agree'), force=True), **kw))
        R = score(SNS(), T); assert R['n_compared'] == 2 and R['agree'] == 1 and abs(R['agree_rate'] - 0.5) < 1e-12, R
        lines.append('3 score: 目視の分類と機械分類の一致と混同の表（一件を変えると一致 1/2）')
        k2 = os.path.join(tmp, 'key-altered.json'); K2 = runs_A.read_json(KP); K2['key'][0]['arm'] = 'X'; json.dump(K2, open(k2, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        try:
            score(SNS(key=k2), T); raise AssertionError('封印と合わない対応表で照合した')
        except SystemExit as ex:
            assert 'SHA-256' in str(ex), ex
        lines.append('4 score: 封印の記録と SHA-256 が合わない対応表で止まる')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print('sample_inspection_A.py %s SELFTEST PASS' % VERSION); print('\n'.join(lines))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest='cmd', required=True)
    e = sub.add_parser('extract'); e.add_argument('--tag', required=True); e.add_argument('--phase', default=None, choices=[None, 'pilot', 'main']); e.add_argument('--root', default=None)
    e.add_argument('--contrasts', default=None); e.add_argument('--out-prefix', default=None); e.add_argument('--force', action='store_true'); e.add_argument('--allow-dry', action='store_true'); e.add_argument('--keydir', default=None)
    s = sub.add_parser('score'); s.add_argument('--seal', required=True); s.add_argument('--key', required=True); s.add_argument('--visual', required=True); s.add_argument('--contrasts', default=None)
    s.add_argument('--out', default=None); s.add_argument('--force', action='store_true')
    sub.add_parser('selftest')
    a = ap.parse_args()
    if a.cmd == 'selftest':
        _selftest()
    else:
        T = runs_A.load_T(a.contrasts)
        extract(a, T) if a.cmd == 'extract' else score(a, T)
