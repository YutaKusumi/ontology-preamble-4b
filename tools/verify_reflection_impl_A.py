# -*- coding: utf-8 -*-
"""verify_reflection_impl_A.py v1 —— 器材の実装検分の反映（採否表 P75〜P104・登録者裁定 D16〜D25）が直ったことを機械で確かめ、
records/reviews/A/draft7-impl/verification-reflection-impl-A.{md,json} を書く（2026-09-14）。
直った条件は事前登録（records/reviews/A/draft7-impl/preregistration-reflection-impl-A.md・一部は事後と開示）。本器は、自己検査・合成検査の記録・起動器の DRY 検査（写しの木）・
合成の走行の上の否定の経路（集計器・応答様式・抽出検査・報告の組み立て器と走査器）・凍結器の一覧・正本と草案と記録の文言の突合を走らせる。
公開 API への問い合わせ（重みの版の解決）は --hf を付けたときだけ行う（資格情報を使わない GET）。リポジトリの results/ と records の現物は変えない（写しと一時置き場で走らせる）。
用法: python tools/verify_reflection_impl_A.py --work <一時置き場> [--hf]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, shutil, subprocess, datetime, glob, argparse, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
REPO = runs_A.REPO
VERSION = 'v1'
ap = argparse.ArgumentParser(); ap.add_argument('--work', required=True); ap.add_argument('--hf', action='store_true'); ap.add_argument('--draft', default='design/design-stageA-draft8.md')
ap.add_argument('--out', default=os.path.join(REPO, 'records', 'reviews', 'A', 'draft7-impl', 'verification-reflection-impl-A'))
a = ap.parse_args()
WORK = os.path.abspath(a.work); assert not os.path.abspath(WORK).startswith(os.path.abspath(REPO)), '一時置き場をリポジトリの中に置かない'
shutil.rmtree(WORK, ignore_errors=True); os.makedirs(WORK)
T = runs_A.load_T(); PY = sys.executable; ENV = dict(os.environ, PYTHONIOENCODING='utf-8'); TOOLS = os.path.join(REPO, 'tools')
ANCHOR = next(m['key'] for m in T['models'] if m['anchor']); S = T['seeds']; CAL = T['calibration']; ARMS = T['arms']['preamble']; MID = runs_A.model_ids(T)
ROWS = []


def R(item, cond, method, ok, detail=''):
    ROWS.append({'item': item, 'condition': cond, 'method': method, 'ok': bool(ok), 'detail': str(detail)[:400]}); print('[verify] %s %s — %s %s' % ('○' if ok else '×', item, cond, '' if ok else str(detail)[:300]), flush=True)


def run(args, env=None, timeout=5400):
    p = subprocess.run([PY] + args, capture_output=True, text=True, encoding='utf-8', errors='replace', env=env or ENV, timeout=timeout)
    return p.returncode, (p.stdout or '') + (p.stderr or '')


SRC = lambda rel: open(os.path.join(REPO, rel), encoding='utf-8').read()
tool = lambda name: os.path.join(TOOLS, name)

# ---- 1. 自己検査
rc, out = run([tool('confirm_A.py'), '--selftest'])
R('P99・D16', '門2 の縮小を指定した対比だけに当て、判定不能の p と p* の不一致の値を正本から読む', '確証の共通関数の自己検査', rc == 0 and 'SELFTEST PASS' in out and '門2 の縮小を一対比だけに当てた' in out, out[-300:])
rc, out = run([tool('firth.py')])
R('D18', '集計と格子の当てはめが firth_check.python_control の打ち切りで行われる', 'Firth の自己検査と共通関数・集計器・格子の記録',
  rc == 0 and 'SELFTEST PASS' in out and 'def pplrt(X, y, idx, m=None, **fit_kw):' in SRC('tools/firth.py') and 'firth.pplrt(X, y, 3, m, **R.fit_kw)' in SRC('tools/confirm_A.py') and '**R.fit_kw' in SRC('tools/analyze_A.py'), out[-200:])
PG = runs_A.read_json(os.path.join(REPO, 'records', 'A', 'power-grid-A.json'))
R('D18（格子）', '格子 v3.2 が打ち切りの設定と現行の正本の SHA16 を記帳している', '格子の記録', PG.get('version') == 'v3.2' and PG['inputs'].get('fit_control') == T['firth_check']['python_control']
  and PG['inputs'].get('contrasts_sha16') == runs_A.sha16_file(runs_A.CPATH) and not PG.get('quick'), {k: PG['inputs'].get(k) for k in ('fit_control', 'contrasts_sha16')})
rc, out = run([tool('judge_fragments_A.py'), 'selftest'])
R('P76・D19', '判定者の読み取りを凍結パーサに通す・機械の再計算の突合・鍵の置き場と封印・除外の区分・条件付け・全対の κ', '判定器の自己検査', rc == 0 and 'SELFTEST PASS' in out, out[-300:])
rc, out = run([tool('report_lint.py'), '--selftest'])
R('P96（走査器）', '報告の走査で code span・括弧の年・章・番号・N GB・段 N の数と、偽の機械の区画と、費用の行の別の数を違反にする', '走査器の自己検査', rc == 0 and 'SELFTEST PASS' in out, out[-300:])

# ---- 2. 重みの版（P75）
bs = SRC('tools/colab/boot_stageA.py')
R('P75（起動器）', '起動器が登録の版を完全な SHA に解き、snapshot の名と照合して取得する', '起動器の原稿', 'runs_A.resolve_rev(HF, T, mk)' in bs and "if snap != rv['full']:" in bs and 'snapshot_download(IDS[mk], revision=rv[\'full\'])' in bs)
if a.hf:
    HF = runs_A.read_json(os.path.join(REPO, 'records', 'A', 'hf-models-A.json'))

    class Api:
        def model_info(self, rid, revision):
            with urllib.request.urlopen('https://huggingface.co/api/models/%s/revision/%s' % (rid, revision), timeout=30) as r:
                return type('Info', (), {'sha': json.loads(r.read().decode('utf-8')).get('sha')})()

    class Bad:
        def model_info(self, rid, revision):
            return type('Info', (), {'sha': 'f' * 40})()
    res = {}
    for m in T['models']:
        try:
            res[m['key']] = runs_A.resolve_rev(HF, T, m['key'], api=Api())['full']
        except Exception as ex:
            res[m['key']] = 'error: %s' % ex
    try:
        runs_A.resolve_rev(HF, T, T['models'][0]['key'], api=Bad()); stops = False
    except RuntimeError:
        stops = True
    R('P75（解決）', '七機種の登録の版が公開 API で四十桁の SHA に解け、接頭辞と一致しない値では止まる', '公開 API（資格情報なしの GET）と偽の API',
      all(len(v) == 40 and v.startswith(HF['models'][k]['rev']) for k, v in res.items()) and stops, res)

# ---- 3. 起動器の DRY 検査（写しの木・P77〜P83・P90・D24）
DW = os.path.join(WORK, 'bootdry')


def clone(name):
    d = os.path.join(DW, name)
    for sub in ('tools', 'arms', 'design', os.path.join('records', 'A')):
        shutil.copytree(os.path.join(REPO, sub), os.path.join(d, sub), ignore=shutil.ignore_patterns('__pycache__'))
    return d


DR = clone('repo'); DR2 = clone('repo_fail'); BASE = {k: v for k, v in os.environ.items() if not k.startswith('OP4B_')}; BASE['PYTHONIOENCODING'] = 'utf-8'


def boot(env, repo=None):
    p = subprocess.run([PY, os.path.join(repo or DR, 'tools', 'colab', 'boot_stageA.py')], env=dict(BASE, **env), capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=DW, timeout=3600)
    out = (p.stdout or '') + (p.stderr or ''); return p.returncode, out, (out.strip().splitlines() or [''])[-1]


dry = lambda repo, **kw: dict({'OP4B_DRY': '1', 'OP4B_REPO_DIR': repo, 'OP4B_PERSIST': os.path.join(DW, 'persist-' + os.path.basename(repo))}, **kw)
srec = lambda repo, name: runs_A.read_json(os.path.join(repo, 'results', 'sessions-A', name))
rc, out, last = boot({'OP4B_REPO_DIR': DR, 'OP4B_PHASE': 'identity'})
R('P78', 'DRY でないのに検査用の環境変数があれば止まる', '起動器の DRY 検査', rc == 1 and 'DRY でないのに検査用の環境変数' in out, last)
rc, out, last = boot({'OP4B_PHASE': 'main', 'OP4B_MODEL': '0.6B'})
R('P82', 'データを作る相で固定のコミットが無ければ止まる', '起動器の DRY 検査', rc == 1 and '固定のコミット' in out, last)
rc, out, last = boot({'OP4B_DRY': '1', 'OP4B_PHASE': 'identity'})
R('P78', 'DRY は置き場の指定を要る', '起動器の DRY 検査', rc == 1 and 'OP4B_REPO_DIR' in out, last)
rc, out, last = boot(dry(DR, OP4B_PHASE='pilot', OP4B_MODEL='0.6B', OP4B_ENV_VALUE='第三'))
R('P82', '「第三」は許した機種だけ', '起動器の DRY 検査', rc == 1 and '「第三」だけで' in out, last)
rc, out, last = boot(dry(DR, OP4B_PHASE='identity', OP4B_DRY_N='2'))
s1 = srec(DR, 'idA__4B-2507__s1.json'); c1 = list(s1['counts'].values())[0]; short = c1['n_ok'] < c1['target']
R('P77・P79', '件数がそろわなければ --redo-errors をかけ、なおそろわなければ止まる', '起動器の DRY 検査', (short and rc == 1 and '件数がそろわない' in out and c1['redo_errors'] == 3) or (not short and rc == 0), c1)
rc, out, last = boot(dry(DR, OP4B_PHASE='identity', OP4B_DRY_N='2', OP4B_DRY_ACCEPT_SHORT='1', OP4B_SESSION='2'))
s2 = srec(DR, 'idA__4B-2507__s2.json')
R('P83・D23', 'セッション記録に版・サーバの引数・件数・終了コード・先取りの欄', '起動器の DRY 検査', rc == 0 and s2['boot'] == 'v2' and s2['model_rev_full'] and s2['server_args'] and s2['counts'] and s2['runner_rc'] and 'preemptions' in s2 and 'pip_freeze_sha16' in s2, last)
sys.path.insert(0, os.path.join(DR, 'tools'))
try:
    runs_A.index_runs(T, T['tags']['identity'], os.path.join(DR, 'results'), allow_multi=True); rej = False
except RuntimeError as ex:
    rej = 'dry-run' in str(ex)
R('P78・W75', 'dry-run の走行は読み出しで止まる', '読み出しの関数', rej)
rc, out, last = boot(dry(DR, OP4B_PHASE='main', OP4B_MODEL='0.6B', OP4B_SESSION='1', OP4B_DRY_N='2', OP4B_DRY_BRANCH='pass', OP4B_DRY_ACCEPT_SHORT='1', OP4B_SCENARIOS='N1'))
s = srec(DR, 'stageA__0.6B__s1.json'); mrk = 'stageA__N1__none__seed%d' % S['main']['0.6B']['N1']; want = ('pass',)
if s.get('calibration_verdict') == 'fired':
    R('D24・calibration.timing', '帯を超えたら機種の走行に進まずに止まり、次のセッション番号を案内する', '起動器の DRY 検査', rc == 0 and 'OP4B_SESSION=2' in out and s['run_keys'] == [], last)
    rc, out, last = boot(dry(DR, OP4B_PHASE='main', OP4B_MODEL='0.6B', OP4B_SESSION='2', OP4B_DRY_N='2', OP4B_DRY_BRANCH='pass', OP4B_DRY_ACCEPT_SHORT='1', OP4B_SCENARIOS='N1'))
    s = srec(DR, 'stageA__0.6B__s2.json'); want = ('anomaly', 'retry_pass')
R('P80・P81・P90', '校正の判定は校正帯の関数（やり直しを含む）・seed は規則と一致・files_sha16_lf に校正腕', '起動器の DRY 検査',
  rc == 0 and s.get('calibration_verdict') in want and s.get('calibration_seed_rule_ok') is True and any(k.startswith(T['tags']['calibration'] + '/') for k in s['files_sha16_lf']) and s['run_keys'] == [mrk],
  {k: s.get(k) for k in ('calibration_verdict', 'run_keys')})
os.makedirs(os.path.join(DR2, 'results', 'sessions-A'), exist_ok=True)
json.dump({'tag': 'stageA', 'model': '0.6B', 'session': 1, 'claimed': '2026-09-14T00:00:00Z'}, open(os.path.join(DR2, 'results', 'sessions-A', '_first_point_claim.json'), 'w', encoding='utf-8'))
rc, out, last = boot(dry(DR2, OP4B_PHASE='main', OP4B_MODEL='1.7B', OP4B_SESSION='1', OP4B_DRY_N='2', OP4B_DRY_BRANCH='fail', OP4B_DRY_ACCEPT_SHORT='1', OP4B_SCENARIOS='N1'))
R('D24', '不合格枝で初点が未確立なら、名乗った機種のほかの本走行を始めない', '起動器の DRY 検査', rc == 1 and '初点を名乗った' in out, last)
rc, out, last = boot(dry(DR2, OP4B_PHASE='bridge', OP4B_MODEL='4B', OP4B_SESSION='1', OP4B_DRY_N='2', OP4B_DRY_BRANCH='fail', OP4B_DRY_ACCEPT_SHORT='1'))
R('D24', '不合格枝で初点が未確立なら橋を始めない', '起動器の DRY 検査', rc == 1 and '橋のセッションを始めない' in out, last)
rc, out, last = boot(dry(DR2, OP4B_PHASE='main', OP4B_MODEL='0.6B', OP4B_SESSION='2', OP4B_DRY_N='2', OP4B_DRY_BRANCH='fail', OP4B_DRY_ACCEPT_SHORT='1', OP4B_SCENARIOS='N1'))
s = srec(DR2, 'stageA__0.6B__s2.json')
R('D24', '名乗った機種は次のセッション番号でも始められ、初点になる', '起動器の DRY 検査', rc == 0 and s.get('calibration_verdict') == 'first_point', last)
rc, out, last = boot(dry(DR2, OP4B_PHASE='bridge', OP4B_MODEL='4B', OP4B_SESSION='1', OP4B_DRY_N='2', OP4B_DRY_BRANCH='fail', OP4B_DRY_ACCEPT_SHORT='1'))
s = srec(DR2, 'stageA-bridge__4B__s1.json')
R('D24', '初点の確立の後は橋も始められ、初点と比べる', '起動器の DRY 検査', rc == 0 and s.get('calibration_judged') == 'band_fail_two_sided', last)
rc, out, last = boot(dry(DR, OP4B_PHASE='pilot', OP4B_MODEL='32B', OP4B_ENV_VALUE='第三', OP4B_DRY_N='1', OP4B_DRY_ACCEPT_SHORT='1', OP4B_SCENARIOS='N1'))
s = srec(DR, 'pilotA__32B__s1.json')
R('P82', '32B は「第三」で始められ、同時要求数は if_not_80GB の値', '起動器の DRY 検査', rc == 0 and s['env_value'] == '第三' and s['concurrency'] == T['environments']['32B']['if_not_80GB']['concurrency'], last)

# ---- 4. 合成検査の記録（P100・P101・P88・P89・P91〜P94・D16・D20・D22・D24）
latest = lambda pat: sorted(glob.glob(os.path.join(REPO, 'records', 'A', pat)))[-1]
SA = runs_A.read_json(latest('synth-A-*.json')); paths = {p for r in SA['per_run'] for p in r['paths']}
R('P100', '合成検査 v2 が全行を発火し、行 id・注・除外・refuse の理由の期待と一致し、変異 M1〜M6 をすべて見分ける', '合成検査の記録',
  SA.get('version') == 'v2' and SA.get('full') and not SA['mismatches'] and not SA['rows_not_fired'] and not SA['paths_missing'] and not SA.get('errors') and len(SA['mutations']) == 6 and all(m['detected'] for m in SA['mutations']),
  {'mutations': [(m['name'], m['mismatches']) for m in SA.get('mutations', [])], 'mismatches': len(SA.get('mismatches', []))})
R('P88・P89・D16・D20・D22', '門0.5 不合格の注・残存規模の非連続の注・門2 の縮小の一部・上向きの確証・対照どうしの差の定型の経路が発火する', '合成検査の記録の経路',
  {'identity_fail_note', 'residual_gap_note', 'gate2_partial_shrink', 'upward', 'control_pairs_string', 'refuse_a', 'refuse_b', 'refuse_d', 'style_a_hold', 'one_side_stage2', 'confirmed_multi_scenario'} <= paths, sorted(paths)[:40])
SG = runs_A.read_json(latest('synth-gates-A-*.json'))
R('P81・P90〜P92・P94・P101・D24', '門と校正の合成検査 v2 が全項目で期待と一致する', '門と校正の合成検査の記録', SG.get('version') == 'v2' and SG.get('pass'), [c['check'] for c in SG.get('checks', []) if not c['ok']])

# ---- 5. 集計器の否定の経路・記述族の注・組み立て器と走査器（合成の走 2 の木）
AR = os.path.join(WORK, 'synth2'); rc, out = run([tool('synth_A.py'), '--root', AR, '--runs', '2', '--mutations', 'none', '--keep'])
R('合成の走 2', '合成の走 2（門0.5 不合格・錨帯）が期待と一致する', '合成検査（走 2 のみ・記録は書かない）', rc == 0 and '不一致 0' in out, out[-300:])
root2 = os.path.join(AR, 'run02'); tag = 'synthA02'; rec2 = os.path.join(root2, 'records'); ANP = os.path.join(root2, 'out', 'analysis-%s.json' % tag)
AN = runs_A.read_json(ANP) if os.path.exists(ANP) else {'descriptive': {'A_desc_ncold': []}}
R('P88', '門0.5 不合格の注が記述族の Ncold−N にも付く', '集計の記録', AN['descriptive']['A_desc_ncold'] and all(T['print_strings']['identity_fail_note'] in (x.get('notes') or []) for x in AN['descriptive']['A_desc_ncold']))
R('D20・D22（出力）', '集計の記録に上向きの確証と対照どうしの差の欄がある', '集計の記録', 'upward_confirmed' in AN and 'A_desc_control_pairs' in AN['descriptive'])
BASEC = [tool('analyze_A.py'), '--tag', tag, '--root', root2, '--anchor-tag', tag + '-anchor2', '--bridge-tag', tag + '-bridge', '--api-tag', tag + '-api', '--style', os.path.join(rec2, 'style-%s.json' % tag),
         '--gate', os.path.join(rec2, 'gate-%s.json' % tag), '--B-measurable', '4', '--synth-nonconverged', 'SK:Lneg~Onull', '--force']
neg = lambda extra, nm: run(BASEC + extra + ['--out', os.path.join(WORK, 'neg-' + nm)])
rc, out = neg(['--calib', os.path.join(rec2, 'calib-%s.json' % tag)], 'noid'); R('P85', '門0.5 の記録が無ければ集計器は止まる', '集計器の否定の経路', rc != 0 and '--identity' in out, out[-200:])
rc, out = neg(['--identity', os.path.join(rec2, 'identity-%s.json' % tag)], 'nocalib'); R('P85', '校正帯の記録が無ければ集計器は止まる', '集計器の否定の経路', rc != 0 and '--calib' in out, out[-200:])
FULL = ['--identity', os.path.join(rec2, 'identity-%s.json' % tag), '--calib', os.path.join(rec2, 'calib-%s.json' % tag)]
sp_ = sorted(glob.glob(os.path.join(root2, 'sessions-A', '%s__*.json' % tag)))[0]; shutil.move(sp_, sp_ + '.away')
rc, out = neg(FULL, 'nosess'); shutil.move(sp_ + '.away', sp_); R('P86', 'セッション記録の無い走行キーで集計器は止まる', '集計器の否定の経路', rc != 0 and 'セッション記録の無い走行キー' in out, out[-200:])
stp = os.path.join(rec2, 'style-%s.json' % tag); keep = open(stp, encoding='utf-8').read(); ST = json.loads(keep); first_m = next(iter(ST['cells'])); first_s = next(iter(ST['cells'][first_m])); del ST['cells'][first_m][first_s]['N']
json.dump(ST, open(stp, 'w', encoding='utf-8'), ensure_ascii=False); rc, out = neg(FULL, 'nostyle'); open(stp, 'w', encoding='utf-8').write(keep)
R('P87', '様式の記録のセルが欠ければ集計器は止まる', '集計器の否定の経路', rc != 0 and '様式の記録が試行の件数と合わない' in out, out[-200:])
ad = sorted(glob.glob(os.path.join(root2, tag + '-anchor2', '*')))[0]; tp = glob.glob(os.path.join(ad, 'trials-*.jsonl'))[0]; keep = open(tp, encoding='utf-8').read()
open(tp, 'w', encoding='utf-8').write(''.join((l.replace('"status":"ok"', '"status":"api_error"') if '"arm":"Onull"' in l else l) + '\n' for l in keep.split('\n') if l))
rc, out = neg(FULL, 'anchor0'); open(tp, 'w', encoding='utf-8').write(keep)
R('P91・W60', '錨反復の腕の n_ok が零は帯を超えないに数えず、記録の不足として止まる', '集計器の否定の経路', rc != 0 and '錨反復' in out and 'n_ok が零' in out, out[-200:])
md = sorted(glob.glob(os.path.join(root2, tag, '*')))[0]; mp = os.path.join(md, 'manifest.json'); keep = open(mp, encoding='utf-8').read(); m = json.loads(keep); m['dry_model_rewritten'] = True
json.dump(m, open(mp, 'w', encoding='utf-8')); rc, out = neg(FULL, 'dry'); open(mp, 'w', encoding='utf-8').write(keep)
R('P78', 'dry-run の印のある走行で集計器は止まる', '集計器の否定の経路', rc != 0 and 'dry-run' in out, out[-200:])
RP = os.path.join(WORK, 'report', 'r.md'); os.makedirs(os.path.dirname(RP))
rc, out = run([tool('build_report_A.py'), '--draft', '1', '--analysis', ANP, '--out', RP, '--force'])
txt = open(RP, encoding='utf-8').read() if os.path.exists(RP) else ''; import report_lint
TL = frozenset(open(os.path.join(REPO, T['report_rules']['template']), encoding='utf-8').read().replace('\r\n', '\n').split('\n')); side = runs_A.read_json(report_lint.sidecar_path(RP)) if os.path.exists(report_lint.sidecar_path(RP)) else None
V = report_lint.lint(txt, T, TL, sidecar=side); kinds = sorted({v['kind'] for v in V})
R('P95・W41', '組み立て器が雛形の行を消さない（引数文字列・除外後に判定不能になった対比・パイロット後に報告した (b) 率の句が残る）', '合成の集計で組み立て器',
  all(w in txt for w in ('引数文字列〔arms_string SHA16〕', '除外後に判定不能になった対比', 'パイロット後に報告した (b) 率')), out[-200:])
R('P96・W61', '機械の区画の記録を書き、打ち込んだ数の一覧の欄を冒頭に置き、記入欄のほかの違反で非零', '合成の集計で組み立て器と走査器',
  side is not None and len(side['blocks']) > 0 and '打ち込んだ数の一覧' in txt and ((rc == 0) == (kinds in ([], ['埋め残し']))), {'rc': rc, 'kinds': kinds})
R('P97・W62', '対照腕の表に Wilson の区間・並記表に PPLRT の統計量', '合成の集計で組み立て器', 'Wilson ' in txt and 'PPLRT 統計量' in txt)
lines_ = txt.split('\n'); MB = report_lint.machine_block(T); ib = next(i for i, l in enumerate(lines_) if MB['begin'] in l); lines_[ib + 1] = lines_[ib + 1] + ' 確証 99 本'
V2 = report_lint.lint('\n'.join(lines_), T, TL, sidecar=side)
R('P96・W42', '機械の区画の中身を書き換えると走査器が記録との不一致を違反にする', '走査器', '機械の区画の中身が記録と違う' in {v['kind'] for v in V2})

# ---- 6. 応答様式と抽出検査（撤退条件の再走を含む合成のパイロット・P84・P93）
PR = os.path.join(WORK, 'pilot'); ptag = T['tags']['pilot']; scen_sha = runs_A.sha16_file(os.path.join(REPO, 'arms', 'frozen-from-ryokai-os', 'app-scenarios.json'))


def pilot_run(mk, sc, seed, sha=None):
    rk = '%s__%s__none__seed%d' % (ptag, sc, seed); d = os.path.join(PR, ptag, rk); os.makedirs(d, exist_ok=True); mfn = MID[mk].replace('/', '_')
    json.dump({'tag': ptag, 'scenario': sc, 'model': MID[mk], 'seed': seed, 'arms': ARMS, 'arm_src': {}, 'scenario_sha': sha or scen_sha}, open(os.path.join(d, 'manifest.json'), 'w', encoding='utf-8'))
    with open(os.path.join(d, 'trials-%s.jsonl' % mfn), 'w', encoding='utf-8') as ft, open(os.path.join(d, 'raw-%s.jsonl' % mfn), 'w', encoding='utf-8') as fr:
        for arm in ARMS:
            for j in range(2):
                tid = '%s-%s-%d' % (rk, arm, j)
                ft.write(json.dumps({'trial_id': tid, 'arm': arm, 'status': 'ok', 'catastrophe': False, 'format_fail': False, 'choice': 'b'}) + '\n')
                fr.write(json.dumps({'trial_id': tid, 'raw_output': ('```json\n{"choice": "b"}\n```' if j == 0 else '考えます。\n```json\n{"choice": "b"}\n```')}, ensure_ascii=False) + '\n')
    return d


s0 = S['pilot'][ANCHOR][CAL['scenario']]; pilot_run(ANCHOR, CAL['scenario'], s0); pilot_run(ANCHOR, CAL['scenario'], s0 + S['rerun_offset']); pilot_run('0.6B', 'N1', S['pilot']['0.6B']['N1'])
rc, out = run([tool('response_mode_A.py'), '--tag', ptag, '--root', PR, '--out', os.path.join(WORK, 'style-pilot.json'), '--force'])
SJ = runs_A.read_json(os.path.join(WORK, 'style-pilot.json')) if rc == 0 else {}
regk = '%s__%s__none__seed%d' % (ptag, CAL['scenario'], s0)
R('P84・W40・W63', '応答様式の器が撤退条件の再走を含むパイロットで止まらず、走行キーごとに数え、cells に登録の seed の走行を置き、名の語彙の出所と場面ファイルの SHA16 を記録する', '合成のパイロットで応答様式の器',
  rc == 0 and len(SJ.get('runs', {})) == 3 and SJ['cells'][ANCHOR][CAL['scenario']] == SJ['runs'][regk]['cells'] and SJ.get('names_source', {}).get('path') == 'tools/response_mode_M.py' and SJ.get('scenario_file_sha16') == scen_sha, out[-200:])
bad = pilot_run('0.6B', 'N1', S['pilot']['0.6B']['N1'], sha='0000000000000000')
rc, out = run([tool('response_mode_A.py'), '--tag', ptag, '--root', PR, '--out', os.path.join(WORK, 'style-pilot-bad.json'), '--force']); pilot_run('0.6B', 'N1', S['pilot']['0.6B']['N1'])
R('P84', '場面ファイルの SHA16 が manifest と違えば応答様式の器は止まる', '合成のパイロットで応答様式の器', rc != 0 and '場面ファイルの SHA16' in out, out[-200:])
rc, out = run([tool('sample_inspection_A.py'), '--tag', ptag, '--phase', 'pilot', '--root', PR, '--out-prefix', os.path.join(WORK, 'si'), '--force'])
samp = open(os.path.join(WORK, 'si-sample.txt'), encoding='utf-8').read() if rc == 0 else ''; heads = [l for l in samp.split('\n') if l.startswith('=== ')]
KJ = runs_A.read_json(os.path.join(WORK, 'si-key.json')) if rc == 0 else {'key': []}
R('P93・W71・W74', '抽出検査の標本は伏せた標識で並び（機種と腕の名を印字しない）、対応表は別のファイルで、再走の走行も枠に入る', '合成のパイロットで抽出検査の器',
  rc == 0 and heads and all(h.startswith('=== S') and not any((' %s ' % arm) in h or ('| %s |' % arm) in h for arm in ARMS) and MID[ANCHOR] not in h for h in heads)
  and len(KJ['key']) == len(heads) and any(k['run_key'].endswith('seed%d' % (s0 + S['rerun_offset'])) for k in KJ['key']), out[-200:])

# ---- 7. 凍結器（P98）
import freeze_A
fl = freeze_A.file_list(a.draft); need = ['design/design-stageA-draft8.src.md', 'arms/materials-draft/hei/refuse-rules-v2.json', 'arms/materials-draft/hei/incentive-lexicon-v2.json', 'arms/panelF/SHA-LEDGER-F.json',
                                        'arms/panelM/SHA-LEDGER-M.json', 'records/F/style-stageF1.json', 'records/A/tooling-interpretations-A.md', 'tools/response_mode_M.py', 'tools/response_mode_F.py']
cost = [f for f in fl if f.startswith('records/cost-pilot/')]
R('P98・W43', '凍結範囲に走行器の語彙と refuse の規則・台帳・転記行 F と G の入力・運用の解釈の一覧・名の語彙の出所があり、原稿は凍結本文の名から決まる', '凍結器の一覧', all(x in fl for x in need) and cost and 'design/design-stageA-draft7.src.md' not in fl, [x for x in need if x not in fl])
R('P98・W56', '枠の検証は見出しの名の完全一致', '凍結器の枠の検証', not freeze_A.frames_check(T) and "names.count(f) != 1" in SRC('tools/freeze_A.py'), freeze_A.frames_check(T))

# ---- 8. 正本・草案・記録の文言（P102・P103・D16〜D25）


def resolve(path, prev):
    def get(p):
        v = T
        for seg in p.split('.'):
            if not isinstance(v, dict) or seg not in v:
                return None
            v = v[seg]
        return v
    cands = [path] + (['.'.join(prev.split('.')[:i]) + '.' + path for i in range(len(prev.split('.')) - 1, 0, -1)] if prev else [])
    for c in cands:
        if get(c) not in (None, '', [], {}):
            return c
    hits = []

    def walk(v, p):
        if isinstance(v, dict):
            for k, x in v.items():
                q = p + '.' + k if p else k
                if q.endswith('.' + path) or q == path:
                    hits.append(q)
                walk(x, q)
    walk(T, '')
    return hits[0] if len(hits) == 1 and get(hits[0]) not in (None, '', [], {}) else None


miss = []
for it in T['registrant_decisions_D16_D25']['items']:
    prev = None
    for seg in it.split(' ', 1)[1].split('・'):
        full = resolve(seg, prev)
        if full is None:
            miss.append((it.split(' ')[0], seg))
        else:
            prev = full
R('D16〜D25（正本）', '登録者裁定 D16〜D25 の文言が正本のキーにある', '正本のキーの突合', not miss, miss)
d8src = SRC('design/design-stageA-draft8.src.md'); d8 = SRC(a.draft) if os.path.exists(os.path.join(REPO, a.draft)) else ''
R('P102・W64', '草案の refuse 門の文が「答えた分母〔refuse を除く n_ok〕が各セルで下限以上」', '草案8 の原稿と組み立て',
  '答えた分母が各セルで {{families/A_slope/refuse_gate/answered_min_n_ok}} 以上を要件' in d8src and '答えた分母が各セルで' in d8 and '各セル n_ok が' not in d8src)
lint8 = os.path.join(REPO, 'records', 'A', 'numbers-lint-draft8A.md')
R('草案8（数の検査）', '草案8 の組み立ての数の検査の違反が零', '数の検査の記録', os.path.exists(lint8) and '違反の合計: 0' in open(lint8, encoding='utf-8').read())
R('D16・D17・D21・D22・D24・D25（草案8）', '草案8 に裁定の文言が入っている', '草案8 の原稿',
  all(w in d8src for w in ('残らない場面の対比だけを判定不能', '傾きの族の全対比に当てる', '文言は裁定 D21', '裁定 D22', '裁定 D24', '裁定 D25', 'D16 門2 の縮小は残らない場面の対比だけを判定不能にする')))
ti = SRC('records/A/tooling-interpretations-A.md')
R('P103', '運用の解釈の記録の「変えていないもの」の文言と追補の項', '運用の解釈の記録',
  '札の入力を決める運用の読み（門2 の数え方・測定不能の走行・錨帯の比べ方・環境値）を含む' in ti and all(('`%s`' % k) in ti for k in ('style_gate.applies_sizes', 'calibration.incomplete_rule', 'sessions.commit_rule'))
  and runs_A.sha16_file(runs_A.CPATH) in ti)
R('W53・D21', '環境帯の引き直しの文言が「パイロットの率が無い腕」', '正本', 'パイロットの率が無い腕' in T['environment_band']['pilot_recheck'])
R('W69・D24', '校正の帰結の文言が timing と withdrawal.rerun を指す', '正本', 'calibration.timing に従う' in T['calibration']['consequence'] and 'calibration.withdrawal.rerun に従う' in T['calibration']['withdrawal']['consequence'])
R('W57・D23', 'セッション記録の欄に pip freeze の SHA・サーバの引数・重みの完全な版・先取りの回数', '正本と起動器', all(f in T['sessions']['fields'] for f in ('pip_freeze_sha16', 'server_args', 'model_rev_full', 'preemptions')))
R('W73・P92', '整合検査がパイロットの再走の seed を撤退条件のセルだけに許す', '整合検査の器', "(mk, sc) == (ANCHOR, T['calibration']['scenario'])" in SRC('tools/integrity_A.py'))
R('W36・P78', 'OP4B_DRY_N を DRY のときだけ読む', '起動器の原稿', "VLLM = os.environ.get('OP4B_VLLM', '0.29.0'); ENV_OVERRIDE = os.environ.get('OP4B_ENV_VALUE'); DRY_N" not in bs and "    DRY_N = int(os.environ.get('OP4B_DRY_N', '0') or 0)" in bs)

ok = all(r['ok'] for r in ROWS)
RES = {'kind': 'verification_reflection_impl_A', 'version': VERSION, 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), 'hf': a.hf, 'pass': ok, 'rows': ROWS,
       'inputs': {'contrasts_sha16': runs_A.sha16_file(runs_A.CPATH), 'synth_A': os.path.basename(latest('synth-A-*.json')), 'synth_gates_A': os.path.basename(latest('synth-gates-A-*.json')),
                  'preregistration_sha16': runs_A.sha16_file(os.path.join(REPO, 'records', 'reviews', 'A', 'draft7-impl', 'preregistration-reflection-impl-A.md'))},
       'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
json.dump(RES, open(a.out + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
M = ['# 反映の確かめ（器材の実装検分の採否表 P75〜P104・登録者裁定 D16〜D25・機械生成・`tools/verify_reflection_impl_A.py` %s・%s UTC）' % (VERSION, RES['generated_utc']), '',
     '- 事前登録: `records/reviews/A/draft7-impl/preregistration-reflection-impl-A.md`（SHA16 %s・一部は事後と開示）。' % RES['inputs']['preregistration_sha16'],
     '- 入力: 正本 SHA16 %s・合成検査の記録 %s・門と校正の合成検査の記録 %s・公開 API の問い合わせ %s。' % (RES['inputs']['contrasts_sha16'], RES['inputs']['synth_A'], RES['inputs']['synth_gates_A'], 'あり' if a.hf else 'なし'),
     '- 判定: **%s**（%d 項目中 %d 項目が直った条件に一致）。' % ('すべて一致' if ok else '不一致あり', len(ROWS), sum(r['ok'] for r in ROWS)), '',
     '| 項 | 直った条件 | 確かめ | 結果 | 詳細（不一致のとき） |', '|---|---|---|---|---|']
M += ['| %s | %s | %s | %s | %s |' % (r['item'], r['condition'], r['method'], '一致' if r['ok'] else '**不一致**', '' if r['ok'] else r['detail'].replace('|', '／')) for r in ROWS]
M += ['', '## 検分票', '', '- 対象: 採否表 P75〜P104 と登録者裁定 D16〜D25 の反映（器材・正本・草案8・記録）。', '- 段階: 事前登録あり（一部は事後・事前登録の「既に走らせた」の欄）。',
      '- 凍結物の同定: 凍結走行器 v2.7・凍結パーサ・盤の台帳（写しの木で使い、現物は変えない）。', '- 盲検の状態: 該当なし。',
      '- 敵対的検分: 検分者の再現の配置（W33〜W76）を裏返して、直った条件で機械に確かめた。合成検査は器の写しに変異を入れて、見分けることを確かめた。',
      '- 系統の内訳: 確かめはコーディネータ（Claude Opus 5）の器。系統外の目は凍結前の最終検分で受ける。', '- COI 記録: 反映を早く終えたい。印＝直った条件を先に書き、不一致を表の先頭の判定に出す。',
      '- 判定: %s。' % ('反映を確かめた（凍結前の最終検分の束へ）' if ok else '不一致の項を直してから確かめ直す'),
      '- 本検分が確認していないこと: 合成の走行は本物の出力の分布を再現しない。起動器は Colab の実機で走らせていない（GPU の同定・サーバの切替・vLLM の計測値の名前・snapshot の名の照合）。変異は六つだけ。事前登録の一部は事後。', '', RES['clause']]
open(a.out + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(M) + '\n')
print('[verify_reflection_impl_A] %s（%d/%d）written %s.{md,json}' % ('PASS' if ok else 'FAIL', sum(r['ok'] for r in ROWS), len(ROWS), a.out))
sys.exit(0 if ok else 1)
